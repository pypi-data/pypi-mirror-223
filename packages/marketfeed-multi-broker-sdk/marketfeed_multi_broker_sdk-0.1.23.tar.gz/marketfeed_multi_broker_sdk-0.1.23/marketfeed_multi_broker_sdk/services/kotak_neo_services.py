import json
import requests
import base64
import datetime
from marketfeed_multi_broker_sdk.models import Login, Order, OrderResponse
from marketfeed_multi_broker_sdk.enums import Broker, Exchange, TransactionType, ProductType, OrderType, Validity
from marketfeed_multi_broker_sdk.utils.jwt_handler import jwt_decode, jwt_encode
from marketfeed_multi_broker_sdk.utils.env_generator import load_env_value


class _KotakNeoAPIService:
    _SUCCESS = 1
    _ERROR = -1

    def _generate_app_token(self, consumer_key, consumer_secret):
        try:
            base_encoded = base64.b64encode(
                f"{consumer_key}:{consumer_secret}".encode("utf-8")).decode("utf-8")
            url = "https://napi.kotaksecurities.com/oauth2/token"
            data = {
                "grant_type": "client_credentials",
            }
            headers = {
                "Authorization": f"Basic {base_encoded}"
            }

            response = requests.post(url, data=data, headers=headers)

            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['error_description']]

            try:
                return [self._SUCCESS, response_json['access_token']]
            except Exception as e:
                return [self._ERROR, response_json['error_description']]

        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]

    def _generate_view_token(self, auth_token, mobile_number, password):
        try:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}',
            }

            data = {
                "mobileNumber": mobile_number,
                "password": password
            }
            response = requests.post(
                'https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate', headers=headers, data=json.dumps(data))
            response_json = json.loads(response.text)
            if response.status_code != 200 and response.status_code != 201:
                return [self._ERROR, response_json['error']]

            try:
                return [self._SUCCESS, response_json['data']]
            except Exception as e:
                return [self._ERROR, response_json['error']]

        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]

    def _validate_2FA(self, auth_token, one_time_token, mobile_number, mpin):
        try:
            headers = {
                'sid': one_time_token['sid'],
                'Auth': one_time_token['token'],
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}',
            }

            data = {
                "mobileNumber": mobile_number,
                "mpin": mpin
            }

            response = requests.post(
                'https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate', headers=headers, data=json.dumps(data))

            response_json = json.loads(response.text)
            if response.status_code != 200 and response.status_code != 201:
                return [self._ERROR, response_json['error']]

            try:
                return [self._SUCCESS, response_json['data']['token']]
            except Exception as e:
                return [self._ERROR, response_json['error']]
        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]

    def _place_order(self, auth_token, session_token, sid, server, exchange, symbol, quantity, price, trigger_price, disclosed_quantity, product_type, transaction_type, order_type, validity, tag, ordersource):
        try:
            headers = {
                "Sid": sid,
                "Auth": session_token,
                "neo-fin-key": "neotradeapi",
                "Content-Type": "application/x-www-form-urlencoded",
                'Authorization': f'Bearer {auth_token}'
            }
            jData = {
                "am": "NO",
                "dq": disclosed_quantity,
                "es": "nse_cm",
                "mp": "0",
                "pc": product_type,
                "pf": "N",
                "pr": price,
                "pt": order_type,
                "qt": quantity,
                "rt": validity,
                "tp": "0",
                "ts": symbol,
                "tt": transaction_type,
                "os": ordersource,  # MOB / WEB
                "ig": tag,
            }
            payload = f"jData={json.dumps(jData)}"
            response = requests.post(
                f"https://gw-napi.kotaksecurities.com/Orders/2.0/quick/order/rule/ms/place?sId={server}", headers=headers, data=payload)

            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['errMsg']]

            if response_json['stat'] != 'Ok':
                return [self._ERROR, response_json['errMsg']]

            order_no = response_json['nOrdNo']
            return [self._SUCCESS, order_no]
        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]


class KotakNeoAPIServices(_KotakNeoAPIService):
    _BROKER = Broker.KOTAK_NEO

    def KotakNeoLogin(self, client_code, login_details: Login):
        app_token_response = super()._generate_app_token(
            login_details.consumer_key,
            login_details.consumer_secret
        )
        if app_token_response[0] == super()._ERROR:
            return ["", app_token_response[1]]
        auth_token = app_token_response[1]

        one_time_token_response = super()._generate_view_token(
            auth_token=auth_token,
            mobile_number=login_details.mobile,
            password=login_details.password
        )
        if one_time_token_response[0] == super()._ERROR:
            return ["", one_time_token_response[1]]
        one_time_token = one_time_token_response[1]

        session_token_response = super()._validate_2FA(
            auth_token=auth_token,
            one_time_token=one_time_token,
            mobile_number=login_details.mobile,
            mpin=login_details.mpin
        )
        if session_token_response[0] == super()._ERROR:
            return ["", session_token_response[1]]
        session_token = session_token_response[1]

        # The data you want to store
        token_payload = {
            'client_code': client_code,
            'broker': 'KOTAK',
            'auth_token': auth_token,
            'sid': one_time_token['sid'],
            'hsServerId': one_time_token['hsServerId'],
            'session_token': session_token,
            'consumer_key': login_details.consumer_key,
            'consumer_secret': login_details.consumer_secret,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return [jwt_encode(payload=token_payload), "success"]

    def KotakNeoPlaceOrder(self, token, client_code, order_details: Order) -> OrderResponse:
        token = jwt_decode(token)

        place_order_response = super()._place_order(
            auth_token=token['auth_token'],
            session_token=token['session_token'],
            sid=token['sid'],
            server=token['hsServerId'],
            exchange=order_details.exchange.value,
            symbol=order_details.symbol,
            quantity=order_details.quantity,
            price=order_details.price,
            trigger_price=order_details.trigger_price,
            disclosed_quantity=order_details.disclosed_quantity,
            product_type=order_details.product_type.value[self._BROKER],
            transaction_type=order_details.transaction_type.value[self._BROKER],
            order_type=order_details.order_type.value[self._BROKER],
            validity=order_details.validity.value[self._BROKER],
            tag=order_details.tag,
            ordersource=order_details.source
        )
        if place_order_response[0] == super()._ERROR:
            return OrderResponse(order_number="", message=place_order_response[1])
        else:
            return OrderResponse(order_number=place_order_response[1], message="success")


# if __name__ == '__main__':
#     client_code = load_env_value('KOTAK_NEO_CLIENT_CODE')
#     mobile = load_env_value('KOTAK_NEO_CLIENT_MOBILE')
#     password = load_env_value('KOTAK_NEO_PASSWORD')
#     mpin = load_env_value('KOTAK_NEO_MPIN')
#     consumer_key = load_env_value('KOTAK_NEO_CONSUMER_KEY')
#     consumer_secret = load_env_value('KOTAK_NEO_CONSUMER_SECRET')

#     kotak_neo_api_service = KotakNeoAPIServices()
#     token, message = kotak_neo_api_service.KotakNeoLogin(
#         client_code=client_code,
#         login_details=Login(
#             consumer_key=consumer_key,
#             consumer_secret=consumer_secret,
#             mobile=mobile,
#             password=password,
#             mpin=mpin
#         )
#     )
#     # print("TOKEN", token, message)
#     order_response: OrderResponse = kotak_neo_api_service.KotakNeoPlaceOrder(
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
#             tag="",
#             source="API"
#         )
#     )
#     print("ORDER", order_response.order_number, order_response.message)


# python3 -m marketfeed_multi_broker_sdk.services.kotak_neo_services
