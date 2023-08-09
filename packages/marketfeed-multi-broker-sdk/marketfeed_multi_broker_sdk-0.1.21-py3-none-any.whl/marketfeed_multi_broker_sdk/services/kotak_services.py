import json
import requests
import base64
import datetime
from marketfeed_multi_broker_sdk.models import Login, Order
from marketfeed_multi_broker_sdk.enums import Broker, Exchange, TransactionType, ProductType, OrderType, Validity
from marketfeed_multi_broker_sdk.utils.jwt_handler import jwt_decode, jwt_encode
from marketfeed_multi_broker_sdk.utils.env_generator import load_env_value


class _KotakAPIService:
    _SUCCESS = 1
    _ERROR = -1

    def _generate_app_token(self, consumer_key, consumer_secret):
        try:
            base_encoded = base64.b64encode(
                f"{consumer_key}:{consumer_secret}".encode("utf-8")).decode("utf-8")
            url = "https://ctradeapi.kotaksecurities.com/token"
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

    def _generate_one_time_token(self, consumer_key, app_token, client_code, password):
        try:
            headers = {
                'accept': 'application/json',
                'consumerKey': consumer_key,
                'ip': '103.171.98.18',
                'appId': 'APP1',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {app_token}',
            }

            data = {"userid": client_code, "password": password}
            response = requests.post(
                'https://ctradeapi.kotaksecurities.com/apim/session/1.0/session/login/userid', headers=headers, data=json.dumps(data))

            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['fault']['message']]

            try:
                return [self._SUCCESS, response_json['Success']['oneTimeToken']]
            except Exception as e:
                return [self._ERROR, response_json['fault']['message']]

        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]

    def _generate_session(self, consumer_key, app_token, one_time_token):
        try:
            headers = {
                'accept': 'application/json',
                'oneTimeToken': one_time_token,
                'consumerKey': consumer_key,
                'ip': '103.171.98.18',
                'appId': 'APP1',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {app_token}',
            }

            data = {"userid": "SI6517"}

            response = requests.post(
                'https://ctradeapi.kotaksecurities.com/apim/session/1.0/session/2FA/oneTimeToken', headers=headers, data=json.dumps(data))
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['fault']['message']]

            try:
                return [self._SUCCESS, response_json['success']['sessionToken']]
            except Exception as e:
                return [self._ERROR, response_json['fault']['message']]
        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]

    def _place_order(self, consumer_key, app_token, session_token, symbol_token, quantity, price, trigger_price, disclosed_quantity, product_type, transaction_type, order_type, validity, tag):
        try:
            headers = {
                'accept': 'application/json',
                'sessionToken': session_token,
                'consumerKey': consumer_key,
                'ip': '103.171.98.18',
                'appId': 'APP1',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {app_token}',
            }
            data = {
                "instrumentToken": symbol_token,
                "transactionType": transaction_type,
                "quantity": quantity,
                "price": price,
                "product": product_type,
                "validity": validity,
                "variety": "REGULAR",
                "disclosedQuantity": disclosed_quantity,
                "triggerPrice": trigger_price,
                "tag": tag
            }
            response = requests.post(
                'https://ctradeapi.kotaksecurities.com/apim/orders/1.0/orders', headers=headers, json=data)

            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['fault']['message']]

            try:
                return [self._SUCCESS, response_json['success']['sessionToken']]
            except Exception as e:
                return [self._ERROR, response_json['fault']['message']]
        except Exception as e:
            print("EE", e)
            return [self._ERROR, e]


class KotakAPIServices(_KotakAPIService):
    _BROKER = Broker.KOTAK

    def KotakLogin(self, client_code, login_details: Login):
        app_token_response = super()._generate_app_token(
            login_details.consumer_key,
            login_details.consumer_secret
        )
        if app_token_response[0] == super()._ERROR:
            return ["", app_token_response[1]]
        app_token = app_token_response[1]

        one_time_token_response = super()._generate_one_time_token(
            consumer_key=login_details.consumer_key,
            app_token=app_token,
            client_code=client_code,
            password=login_details.password
        )
        if one_time_token_response[0] == super()._ERROR:
            return ["", one_time_token_response[1]]
        one_time_token = one_time_token_response[1]

        session_token_response = super()._generate_session(
            consumer_key=login_details.consumer_key,
            app_token=app_token,
            one_time_token=one_time_token
        )
        if session_token_response[0] == super()._ERROR:
            return ["", session_token_response[1]]
        session_token = session_token_response[1]

        # The data you want to store
        token_payload = {
            'client_code': client_code,
            'broker': 'KOTAK',
            'session_token': session_token,
            'consumer_key': login_details.consumer_key,
            'consumer_secret': login_details.consumer_secret,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return [jwt_encode(payload=token_payload), "success"]

    def KotakPlaceOrder(self, token, client_code, order_details: Order):
        token = jwt_decode(token)
        app_token_response = super()._generate_app_token(
            token['consumer_key'],
            token['consumer_secret']
        )
        if app_token_response[0] == super()._ERROR:
            return ["", app_token_response[1]]
        app_token = app_token_response[1]

        place_order_response = super()._place_order(
            consumer_key=token['consumer_key'],
            app_token=app_token,
            session_token=token['session_token']
        )
        if place_order_response[0] == super()._ERROR:
            return ["", place_order_response[1]]
        else:
            return [place_order_response[1], "success"]


# if __name__ == '__main__':
#     client_code = load_env_value('KOTAK_CLIENT_CODE')
#     password = load_env_value('KOTAK_PASSWORD')
#     consumer_key = load_env_value('KOTAK_CONSUMER_KEY')
#     consumer_secret = load_env_value('KOTAK_CONSUMER_SECRET')


#     kotak_api_service = KotakAPIServices()
#     token, message = kotak_api_service.KotakLogin(
#         client_code=client_code,
#         login_details=Login(
#             consumer_key=consumer_key,
#             consumer_secret=consumer_secret,
#             password=password
#         )
#     )
#     print("TOKEN", token, message)
    # order_number, message = kotak_api_service.KotakPlaceOrder(
    #     token=token,
    #     client_code=client_code,
    #     order_details=None
    # )
    # print("ORDER", order_number, message)


# python3 -m marketfeed_multi_broker_sdk.services.kotak_services
