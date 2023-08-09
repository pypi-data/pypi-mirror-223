import json
import hashlib
import pyotp
import requests
import time
import urllib.parse
from marketfeed_multi_broker_sdk.models import Login, Order, OrderResponse, HoldingData, HoldingResponse, PositionData, PositionResponse
from marketfeed_multi_broker_sdk.enums import Broker, Exchange, TransactionType, ProductType, OrderType, Validity


class _ShoonyaAPIService:

    _BASE_URL = "https://api.shoonya.com/NorenWClientTP"
    _SUCCESS = 1
    _ERROR = -1

    def _start_session(self, client_code, password, two_fa, app_vendor_code, app_imei, app_key):
        try:
            url = f"{self._BASE_URL}/QuickAuth"
            appKey = f"{client_code}|{app_key}"
            jData = {
                "apkversion": "1.0.15",
                "uid": client_code,
                "pwd": hashlib.sha256(password.encode()).hexdigest(),
                "factor2": pyotp.TOTP(two_fa).now(),
                "imei": app_imei,
                "source": "API",
                "vc": app_vendor_code,
                "appkey": hashlib.sha256(appKey.encode()).hexdigest()
            }

            # Convert the dictionary to a JSON-formatted string
            payload = f"jData={json.dumps(jData)}"
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            if response.status_code != 200:
                return [self._ERROR, response.text]

            host_lookup_response_json = json.loads(response.text)
            if host_lookup_response_json['stat'] != 'Ok':
                return [self._ERROR, host_lookup_response_json['emsg']]

            token = host_lookup_response_json['susertoken']
            return [self._SUCCESS, token]
        except Exception as e:
            return [self._ERROR, e]

    def _place_order(self, token, client_code, exchange, symbol, quantity, price, trigger_price, disclosed_quantity, product_type, transaction_type, order_type, validity, tag, ordersource):
        try:
            url = f"{self._BASE_URL}/PlaceOrder"
            jData = {
                "uid": client_code,
                "actid": client_code,
                "exch": exchange,
                "tsym": urllib.parse.quote_plus(symbol),
                "qty": str(quantity),
                "prc": str(price),
                "trgprc": str(trigger_price),
                "dscqty": str(disclosed_quantity),
                "prd": product_type,
                "trantype": transaction_type,
                "prctyp": order_type,
                "ret": validity,
                "remarks": tag,
                "ordersource": ordersource,
            }

            # Convert the dictionary to a JSON-formatted string
            payload = f"jData={json.dumps(jData)}&jKey={token}"
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            if response.status_code != 200:
                return [self._ERROR, response.text]

            host_lookup_response_json = json.loads(response.text)
            if host_lookup_response_json['stat'] != 'Ok':
                return [self._ERROR, host_lookup_response_json['emsg']]

            order_no = host_lookup_response_json['norenordno']
            return [self._SUCCESS, order_no]
        except Exception as e:
            return [self._ERROR, e]

    def _holding(self, token, client_code):
        try:
            url = f"{self._BASE_URL}/Holdings"
            jData = {
                "uid": client_code,
                "actid": client_code,
                "prd": "C"  # C / M / I / B / H
            }

            # Convert the dictionary to a JSON-formatted string
            payload = f"jData={json.dumps(jData)}&jKey={token}"
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            print(response.status_code)
            print(response.text)
            if response.status_code != 200:
                return [self._ERROR, response.text]
            response_json = json.loads(response.text)
            print(response_json)
            print("A")
            return response_json

            holdings_data = response_json['exch_tsym']
            holdings_list = []
            for key, value in holdings_data.items():
                holding_data: HoldingData = HoldingData(
                    symbol=value['ISIN'],
                    symbol_token=str(value['ExchangeNSEInstrumentId']),
                    quantity=value['HoldingQuantity'],
                    average_price=value['BuyAvgPrice']
                )
                holdings_list.append(holding_data)
            return [self._SUCCESS, holdings_list]
        except Exception as e:
            return [self._ERROR, e]

    def _position(self, token, client_code):
        try:
            url = f"{self._BASE_URL}/PositionBook"
            jData = {
                "uid": client_code,
                "actid": client_code,
            }

            # Convert the dictionary to a JSON-formatted string
            payload = f"jData={json.dumps(jData)}&jKey={token}"
            headers = {
                'Content-Type': 'application/json',
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            if response.status_code != 200:
                return [self._ERROR, response.text]
            response_json = json.loads(response.text)

            positions_list = []
            for value in response_json:
                position_data: PositionData = PositionData(
                    symbol=value['tsym'],
                    symbol_token=str(value['token']),
                    quantity=abs(int(value['netqty'])),
                    transaction_type="BUY" if int(
                        value['netqty']) > 0 else "SELL",
                    buy_average=float(value['daybuyavgprc']),
                    sell_average=float(value['daysellavgprc'])
                )
                positions_list.append(position_data)
            return [self._SUCCESS, positions_list]
        except Exception as e:
            return [self._ERROR, e]


class ShoonyaAPIServices(_ShoonyaAPIService):
    _BROKER = Broker.SHOONYA

    def ShoonyaLogin(self, client_code, login_details: Login):
        for i in range(1, 3):
            start_session_response = super()._start_session(
                client_code=client_code,
                password=login_details.password,
                two_fa=login_details.totp_key,
                app_vendor_code=login_details.app_vendor,
                app_imei=login_details.app_imei,
                app_key=login_details.app_key
            )
            if start_session_response[0] != super()._SUCCESS:
                time.sleep(1)
            else:
                break
        if start_session_response[0] == super()._ERROR:
            return ["", start_session_response[1]]
        else:
            return [start_session_response[1], "success"]

    def ShoonyaPlaceOrder(self, token, client_code, order_details: Order) -> OrderResponse:
        place_order_response = super()._place_order(
            token=token,
            client_code=client_code,
            exchange=order_details.exchange.value,
            symbol=order_details.symbol,
            quantity=order_details.quantity,
            price=order_details.price,
            trigger_price=order_details.trigger_price,
            disclosed_quantity=order_details.disclosed_quantity,
            transaction_type=order_details.transaction_type.value[self._BROKER],
            product_type=order_details.product_type.value[self._BROKER],
            order_type=order_details.order_type.value[self._BROKER],
            validity=order_details.validity.value[self._BROKER],
            tag=order_details.tag,
            ordersource=order_details.source
        )

        if place_order_response[0] == super()._ERROR:
            return OrderResponse(order_number="", message=place_order_response[1])
        else:
            return OrderResponse(order_number=place_order_response[1], message="success")

    def ShoonyaHolding(self, token, client_code) -> HoldingResponse:
        start_session_response = super()._holding(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return HoldingResponse(
                holding=None,
                message=f"{client_code} start session failure - {start_session_response[1]}"
            )
        return HoldingResponse(holding=start_session_response[1], message="success")

    def ShoonyaPosition(self, token, client_code) -> PositionResponse:
        start_session_response = super()._position(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return PositionResponse(
                position=None,
                message=f"{client_code} start session failure - {start_session_response[1]}"
            )
        return PositionResponse(position=start_session_response[1], message="success")


# if __name__ == '__main__':
#     from marketfeed_multi_broker_sdk.utils.env_generator import load_env_value
#     client_code = load_env_value('SHOONYA_CLIENT_CODE')
#     password = load_env_value('SHOONYA_PASSWORD')
#     totp_key = load_env_value('SHOONYA_TOTP_KEY')
#     app_vendor = load_env_value('SHOONYA_APP_VENDOR')
#     app_imei = load_env_value('SHOONYA_APP_IMEI')
#     app_key = load_env_value('SHOONYA_APP_KEY')

#     shoonyaAPI = ShoonyaAPIServices()
    # token, message = shoonyaAPI.ShoonyaLogin(
    #     client_code=client_code,
    #     login_details=Login(
    #         password=password,
    #         totp_key=totp_key,
    #         app_vendor=app_vendor,
    #         app_imei=app_imei,
    #         app_key=app_key
    #     )
    # )
    # print("TOKEN", token, message)
    # token = "a976ef8712ce0fe86c895ce8a704c7f6646b15f114ba4d78d9f99f550c385c78"

    # holding_response: HoldingResponse = shoonyaAPI.ShoonyaHolding(
    #     token=token, client_code=client_code)
    # print("HOLDING", holding_response.holding, holding_response.message)

    # holding_response: PositionResponse = shoonyaAPI.ShoonyaPosition(
    #     token=token, client_code=client_code)
    # print("POSITION", holding_response.position, holding_response.message)

#     order_response: OrderResponse = shoonyaAPI.ShoonyaPlaceOrder(
#         token=token,
#         client_code=client_code,
#         order_details=Order(
#             exchange=Exchange.NSE,
#             symbol="TATAMOTORS-EQ",
#             quantity=1,
#             price=0,
#             trigger_price=0,
#             disclosed_quantity=0,
#             transaction_type=TransactionType.BUY,
#             product_type=ProductType.INTRADAY,
#             order_type=OrderType.MARKET,
#             validity=Validity.DAY,
#             tag="testing",
#             source="API"
#         )
#     )
#     print("ORDER", order_response.order_number, order_response.message)

# python3 -m marketfeed_multi_broker_sdk.services.shoonya_services
