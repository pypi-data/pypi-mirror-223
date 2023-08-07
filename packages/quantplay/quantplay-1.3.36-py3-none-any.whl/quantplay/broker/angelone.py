import json
import time

import pandas as pd
import pyotp
import websocket
from retrying import retry
from SmartApi import SmartConnect

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.exception.exceptions import QuantplayOrderPlacementException, TokenException, ServiceException
import requests, pickle, codecs
import _thread as thread
from quantplay.utils.pickle_utils import PickleUtils
import numpy as np

from quantplay.utils.constant import Constants, OrderType


class AngelOne(Broker):

    def __init__(self, order_updates=None, api_key=None, user_id=None, mpin=None, totp=None, wrapper=None):
        super(AngelOne, self).__init__()
        self.order_updates = order_updates

        try:
            if wrapper:
                self.set_wrapper(wrapper)
            else:
                self.wrapper = SmartConnect(api_key=self.api_key)
                self.wrapper.generateSession(user_id, mpin, pyotp.TOTP(totp).now())
        except Exception as e:
            raise TokenException(str(e))

        token_data = self.wrapper.generateToken(self.wrapper.refresh_token)

        self.refresh_token = token_data['data']['refreshToken']
        self.jwt_token = token_data['data']['jwtToken']
        self.user_id = self.wrapper.userId
        self.api_key = self.wrapper.api_key

        self.load_instrument()

    def set_wrapper(self, serialized_wrapper):
        self.wrapper = pickle.loads(codecs.decode(serialized_wrapper.encode(), "base64"))

    def on_message(self, ws, order):
        try:
            order = json.loads(order)

            order['placed_by'] = self.user_id
            order['tag'] = self.user_id
            order['order_id'] = order['orderid']
            order['exchange_order_id'] = order['order_id']
            order['transaction_type'] = order['transactiontype']
            order['quantity'] = int(order['quantity'])
            order['order_type'] = order['ordertype']

            if order['exchange'] == "NFO":
                order["tradingsymbol"] = self.symbol_map[order["tradingsymbol"]]

            if order['order_type'] == "STOPLOSS_LIMIT":
                order['order_type'] = "SL"

            if 'triggerprice' in order and order['triggerprice'] != 0:
                order['trigger_price'] = float(order['triggerprice'])
            else:
                order['trigger_price'] = None

            if order["status"] == "trigger pending":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "cancelled":
                order["status"] = "CANCELLED"
            elif order["status"] == "open":
                order["status"] = "OPEN"
            elif order["status"] == "complete":
                order["status"] = "COMPLETE"

            self.order_updates.put(order)
        except Exception as e:
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
        print(json.dumps(order))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for i in range(300000):
                time.sleep(1)
                ws.send(json.dumps({
                    "actiontype": "subscribe",
                    "feedtype": "order_feed",
                    "jwttoken": self.jwt_token,
                    "clientcode": self.user_id,
                    "apikey": self.api_key
                }))
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    def load_instrument(self):
        try:
            self.symbol_data = PickleUtils.load_data("angelone_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            symbol_data = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
            data = requests.get(symbol_data)
            inst_data = json.loads(data.content)
            inst_data = pd.DataFrame(inst_data)
            self.instrument_data = inst_data[(inst_data.exch_seg.isin(["NFO", "MCX", "CDS"])) | (
                    (inst_data.exch_seg == "NSE") & (inst_data.symbol.str.contains("-EQ")))]

            self.instrument_data.loc[:, 'instrument_symbol'] = self.instrument_data.name
            self.instrument_data.loc[:, 'instrument_expiry'] = self.instrument_data.expiry
            self.instrument_data.loc[:, 'instrument'] = self.instrument_data.instrumenttype
            self.instrument_data.loc[:, 'strike_price'] = self.instrument_data.strike.astype(float) / 100
            self.instrument_data.loc[:, 'exchange'] = self.instrument_data.exch_seg
            self.instrument_data.loc[:, 'option_type'] = np.where("PE" == self.instrument_data.symbol.str[-2:], "PE",
                                                                  "CE")
            self.instrument_data.loc[:, 'option_type'] = np.where(self.instrument_data.instrument.str.contains("OPT"),
                                                                  self.instrument_data.option_type,
                                                                  None)

            self.initialize_expiry_fields()
            self.add_quantplay_fut_tradingsymbol()
            self.add_quantplay_opt_tradingsymbol()

            self.instrument_data = self.instrument_data[['token', 'symbol', 'strike_price', 'exchange',
                                                         'option_type', 'instrument', 'tradingsymbol', 'expiry']]
            self.instrument_data.loc[:, 'broker_symbol'] = self.instrument_data.symbol

            self.initialize_symbol_data(save_as="angelone_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    def get_order_type(self, order_type):
        if order_type == OrderType.sl:
            return "STOPLOSS_LIMIT"
        elif order_type == OrderType.slm:
            return "STOPLOSS_MARKET"

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return "CARRYFORWARD"
        elif product == "CNC":
            return "DELIVERY"
        elif product == "MIS":
            return "INTRADAY"
        elif product in ["BO", "MARGIN"]:
            return product

        raise InvalidArgumentException("Product {} not supported for trading".format(product))

    def stream_order_data(self):
        root_url = "smartapisocket.angelbroking.com/websocket"
        ws_url = "wss://{}?jwttoken={}&clientcode={}&apikey={}".format(
            root_url,
            self.jwt_token,
            self.user_id, self.api_key)

        websocket.enableTrace(False)
        print(ws_url)
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error)
        ws.on_open = self.on_open
        ws.run_forever()

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_ltp(self, exchange=None, tradingsymbol=None):
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[tradingsymbol]

        symbol_data = self.symbol_data[f"{exchange}:{self.get_symbol(tradingsymbol)}"]
        symboltoken = symbol_data['token']

        if exchange == "NSE" and tradingsymbol not in ["NIFTY", "BANKNIFTY"]:
            tradingsymbol = "{}-EQ".format(tradingsymbol)

        response = self.wrapper.ltpData(exchange, tradingsymbol, symboltoken)
        if 'status' in response and response['status'] == False:
            raise InvalidArgumentException("Failed to fetch ltp broker error {}".format(response))

        return response['data']['ltp']

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        try:
            if trigger_price == 0:
                trigger_price = None

            order_type = self.get_order_type(order_type)
            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)

            symbol_data = self.symbol_data[f"{exchange}:{self.get_symbol(tradingsymbol)}"]
            symbol_token = symbol_data['token']

            order = {
                "transactiontype": transaction_type,
                "variety": "NORMAL",
                "tradingsymbol": tradingsymbol,
                "ordertype": order_type,
                "triggerprice": trigger_price,
                "exchange": exchange,
                "symboltoken": symbol_token,
                "producttype": product,
                "price": price,
                "quantity": quantity,
                "duration": "DAY",
                "ordertag": tag
            }

            print("[PLACING_ORDER] {}".format(json.dumps(order)))
            return self.wrapper.placeOrder(order)
        except Exception as e:
            raise QuantplayOrderPlacementException(str(e))

    def positions(self):
        positions = self.wrapper.position()

        if positions['data'] is None:
            return pd.DataFrame(columns=self.positions_column_list)

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def orders(self, tag=None, status=None):
        order_book = self.wrapper.orderBook()
        if order_book['data']:
            orders = pd.DataFrame(order_book['data'])

            positions = self.positions()
            if len(orders) == 0:
                return pd.DataFrame(columns=self.orders_column_list)

            positions = positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
            orders = pd.merge(orders, positions[['tradingsymbol', 'ltp']],
                              how="left",
                              left_on=['tradingsymbol'],
                              right_on=['tradingsymbol'])

            orders.rename(
                columns={
                    'orderid': 'order_id',
                    'uid': self.user_id,
                    'ordertag': 'tag',
                    'averageprice': 'average_price',
                    'producttype': 'product',
                    'transactiontype': 'transaction_type',
                    "triggerprice": "trigger_price",
                    "price": "price",
                    'filledshares': 'filled_quantity',
                    'unfilledshares': 'pending_quantity',
                    'updatetime': 'order_timestamp',
                    'info': 'text'

                }, inplace=True)

            existing_columns = list(orders.columns)
            columns_to_keep = list(set(self.orders_column_list).intersection(set(existing_columns)))
            orders = orders[columns_to_keep]

            orders.loc[:, 'order_timestamp'] = pd.to_datetime(orders.order_timestamp)
            orders = self.filter_orders(orders, status=status, tag=tag)
            return orders
        else:
            if 'errorcode' in order_book and order_book['errorcode'] == "AB1010":
                raise TokenException("Can't Fetch order book because session got expired")
            else:
                raise ServiceException("Unknown error while fetching order book [{}]")

    def profile(self):
        profile_data = self.wrapper.getProfile(self.refresh_token)['data']
        response = {
            'user_id': profile_data['clientcode'],
            'full_name': profile_data['name'],
            'email': profile_data['email']
        }

        return response

    def account_summary(self):
        margins = self.wrapper.rmsLimit()['data']

        pnl = 0
        # positions = self.positions()
        # if len(positions) > 0:
        #     pnl = positions.pnl.sum()

        response = {
            'margin_used': margins['net'],
            'total_balance': margins['net'],
            'margin_available': margins['net'],
            'pnl': pnl
        }
        return response
