import requests
import json
import pyotp
import time
import hashlib
from urllib.parse import parse_qs, urlparse
from marketfeed_multi_broker_sdk.models import Login, Order, OrderResponse, MarginData, MarginResponse, HoldingData, HoldingResponse, PositionData, PositionResponse
from marketfeed_multi_broker_sdk.enums import Broker, Exchange, TransactionType, ProductType, OrderType, Validity


class _FyersAPIService:

    _BASE_URL = "https://api-t2.fyers.in/vagator/v2"
    _BASE_URL_2 = "https://api.fyers.in/api/v2"
    _APP_ID = "HS9UNQO5PR"
    _SECRET_KEY = "9ISNH40B7S"
    _REDIRECT_URI = "https://asia-south1-marketfeed-stage.cloudfunctions.net/fyersRedirectUrl"
    _APP_TYPE = "102"
    _CLIENT_ID = f'{_APP_ID}-{_APP_TYPE}'

    _SUCCESS = 1
    _ERROR = -1

    def _send_login_otp(self, client_id):
        try:
            url = f'{self._BASE_URL}/send_login_otp'
            data = {"fy_id": client_id, "app_id": self._APP_ID}
            response = requests.post(url, json=data)

            if response.status_code != 200:
                return [self._ERROR, response.text]
            result = json.loads(response.text)
            request_key = result["request_key"]
            return [self._SUCCESS, request_key]
        except Exception as e:
            return [self._ERROR, e]

    def _verify_totp(self, request_key, totp):
        try:
            url = f'{self._BASE_URL}/verify_otp'
            data = {"request_key": request_key, "otp": totp}
            response = requests.post(url, json=data)
            if response.status_code != 200:
                return [self._ERROR, response.text]
            result = json.loads(response.text)
            request_key = result["request_key"]
            return [self._SUCCESS, request_key]
        except Exception as e:
            return [self._ERROR, e]

    def _verify_pin(self, request_key, pin):
        try:
            url = f'{self._BASE_URL}/verify_pin'
            data = {"request_key": request_key, "identity_type": "pin",
                    "identifier": f"{pin}", "recaptcha_token": ""}
            response = requests.post(url, json=data)
            if response.status_code != 200:
                return [self._ERROR, response.text]
            result = json.loads(response.text)
            access_token = result["data"]['access_token']
            return [self._SUCCESS, access_token]
        except Exception as e:
            return [self._ERROR, e]

    def _generate_token(self, access_token, client_id):
        try:
            url = f'{self._BASE_URL_2}/token'
            headers = {
                "authorization": f"Bearer {access_token}"
            }
            data = {"fyers_id": client_id, "app_id": self._APP_ID, "redirect_uri": self._REDIRECT_URI, "appType": self._APP_TYPE,
                    "code_challenge": "", "state": "None", "scope": "", "nonce": "", "response_type": "code", "create_cookie": True}
            response = requests.post(url, headers=headers, json=data)
            result = json.loads(response.text)
            url = result["Url"]
            parsed = urlparse(url)
            auth_code = parse_qs(parsed.query)['auth_code'][0]
            return [self._SUCCESS, auth_code]
        except Exception as e:
            return [self._ERROR, e]

    def _get_hash(self):
        hash_val = hashlib.sha256(
            (self._CLIENT_ID+":"+self._SECRET_KEY).encode())
        return hash_val.hexdigest()

    def _validate_token(self, access_token, auth_token):
        url = f'{self._BASE_URL_2}/validate-authcode'
        headers = {
            "authorization": f"Bearer {access_token}"
        }
        data = {"grant_type": "authorization_code",
                "appIdHash": self._get_hash(), "code": auth_token}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return [self._ERROR, response.text]
        result = json.loads(response.text)
        access_token = result["access_token"]
        return [self._SUCCESS, access_token]

    def _margin(self, token, client_code):
        try:
            response = requests.get(
                f'{self._BASE_URL_2}/funds',
                headers={
                    'Authorization': f'{self._CLIENT_ID}:{token}',
                },
            )
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['message']]

            if response_json['s'] != 'ok':
                return [self._ERROR, response_json['message']]

            balance_list = response_json['fund_limit']
            # Define the titles you are interested in
            titles = ['Total Balance', 'Utilized Amount', 'Available Balance']

            # Create a dictionary with your selected titles and their equity amounts
            new_result = {
                item['title'].replace(' ', '_').lower(): item['equityAmount']
                for item in balance_list if item['title'] in titles
            }
            margin_data: MarginData = MarginData(
                available_balance=float(new_result['total_balance']),
                utilized_balance=float(new_result['utilized_amount']),
                remaining_balance=float(new_result['available_balance'])
            )
            return [self._SUCCESS, margin_data]
        except Exception as e:
            return [self._ERROR, e]

    def _place_order(self, token, client_code, exchange, symbol, quantity, price, trigger_price, disclosed_quantity, product_type, transaction_type, order_type, validity, tag, ordersource):
        try:
            url = f"{self._BASE_URL_2}/orders"
            headers = {
                'Authorization': f'{self._CLIENT_ID}:{token}',
            }
            payload = {
                "symbol": f"{exchange}:{symbol}",
                "qty": quantity,
                "type": order_type,
                "side": transaction_type,
                "productType": product_type,
                "limitPrice": price,
                "stopPrice": 0,
                "disclosedQty": disclosed_quantity,
                "validity": validity,
                "offlineOrder": "False",
                "stopLoss": 0,
                "takeProfit": 0
            }
            response = requests.request(
                "POST", url, headers=headers, json=payload)
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['message']]

            if response_json['s'] != 'ok':
                return [self._ERROR, response_json['message']]

            order_no = response_json['id']
            return [self._SUCCESS, order_no]
        except Exception as e:
            return [self._ERROR, e]

    def _holding(self, token, client_code):
        try:
            response = requests.get(
                f'{self._BASE_URL_2}/holdings',
                headers={
                    'Authorization': f'{self._CLIENT_ID}:{token}',
                },
            )
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['message']]

            if response_json['s'] != 'ok':
                return [self._ERROR, response_json['message']]

            holdings_data = response_json['holdings']
            holdings_list = []
            for key, value in holdings_data:
                holding_data: HoldingData = HoldingData(
                    symbol=value['symbol'].split(":")[1].split("-")[0],
                    symbol_token=str(value['fyToken']),
                    quantity=value['quantity'],
                    average_price=value['BuyAvgPrice']
                )
                holdings_list.append(holding_data)
            return [self._SUCCESS, holdings_list]
        except Exception as e:
            return [self._ERROR, e]

    def _position(self, token, client_code):
        try:
            response = requests.get(
                f'{self._BASE_URL_2}/positions',
                headers={
                    'Authorization': f'{self._CLIENT_ID}:{token}',
                },
            )
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['message']]

            if response_json['s'] != 'ok':
                return [self._ERROR, response_json['message']]

            positions_data = response_json['netPositions']
            positions_list = []
            for key, value in positions_data:
                position_data: PositionData = PositionData(
                    symbol=value['symbol'].split(":")[1].split("-")[0],
                    symbol_token=str(value['fyToken']),
                    quantity=abs(int(value['qty'])),
                    transaction_type="BUY" if value['side'] == 1 else "SELL",
                    buy_average=float(value['buyAvg']),
                    sell_average=float(value['sellAvg'])
                )
                positions_list.append(position_data)
            return [self._SUCCESS, positions_list]
        except Exception as e:
            return [self._ERROR, e]


class FyersAPIServices(_FyersAPIService):
    _BROKER = Broker.FYERS

    def FyersLogin(self, client_code, login_details: Login):
        send_otp_result = super()._send_login_otp(client_id=client_code)
        if send_otp_result[0] != super()._SUCCESS:
            return ["", f"{client_code} send_login_otp failure - {send_otp_result[1]}"]
        request_key = send_otp_result[1]

        request_key_2 = None
        for i in range(1, 3):
            verify_totp_result = super()._verify_totp(
                request_key=request_key, totp=pyotp.TOTP(login_details.totp_key).now())

            if verify_totp_result[0] != super()._SUCCESS:
                print(f"verify_totp_result failure - {verify_totp_result[1]}")
                time.sleep(1)
            else:
                request_key_2 = verify_totp_result[1]
                break
        if request_key_2 == None:
            return ["", f"{client_code} verify otp failure"]

        verify_pin_result = super()._verify_pin(
            request_key=request_key_2, pin=login_details.pin)
        if verify_pin_result[0] != super()._SUCCESS:
            return ["", f"{client_code} verify pin failure  - {verify_pin_result[1]}"]
        access_token = verify_pin_result[1]

        generate_token_result = super()._generate_token(
            access_token, client_code)
        if generate_token_result[0] != super()._SUCCESS:
            return ["", f"{client_code} generate token failure  - {generate_token_result[1]}"]
        auth_code = generate_token_result[1]

        validate_token_response = super()._validate_token(
            access_token=access_token, auth_token=auth_code)

        if validate_token_response[0] != super()._SUCCESS:
            return ["", f"{client_code} validate token failure  - {validate_token_response[1]}"]

        return [validate_token_response[1], "success"]

    def FyersMargin(self, token, client_code) -> MarginResponse:
        start_session_response = super()._margin(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return MarginResponse(
                margin=None,
                message=f"{client_code} start session failure - {start_session_response[1]}"
            )
        return MarginResponse(margin=start_session_response[1], message="success")

    def FyersPlaceOrder(self, token, client_code, order_details: Order) -> OrderResponse:
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

    def FyersHolding(self, token, client_code) -> HoldingResponse:
        start_session_response = super()._holding(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return HoldingResponse(
                holding=None,
                message=f"{client_code} holding failure - {start_session_response[1]}"
            )
        return HoldingResponse(holding=start_session_response[1], message="success")

    def FyersPosition(self, token, client_code) -> PositionResponse:
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
#     client_code = load_env_value('FYERS_CLIENT_CODE')
#     totp_key = load_env_value('FYERS_TOTP_KEY')
#     pin = load_env_value('FYERS_PIN')

#     fyers_api_service = FyersAPIServices()
#     token, message = fyers_api_service.FyersLogin(
#         client_code=client_code,
#         login_details=Login(
#             totp_key=totp_key,
#             pin=pin
#         )
#     )
#     print("TOKEN", token, message)

    # margin_response: MarginResponse = fyers_api_service.FyersMargin(
    #     token=token, client_code=client_code)
    # print("MARGIN", margin_response.margin, margin_response.message)

    # holding_response: HoldingResponse = fyers_api_service.FyersHolding(
    #     token=token, client_code=client_code)
    # print("HOLDING", holding_response.holding, holding_response.message)

    # position_response: PositionResponse = fyers_api_service.FyersPosition(
    #     token=token, client_code=client_code)
    # print("POSITION", position_response.position, position_response.message)

    # order_response: OrderResponse = fyers_api_service.FyersPlaceOrder(
    #     token=token,
    #     client_code=client_code,
    #     order_details=Order(
    #         exchange=Exchange.NSE,
    #         symbol="TATAMOTORS-EQ",
    #         quantity=1,
    #         price=0,
    #         trigger_price=0,
    #         disclosed_quantity=0,
    #         transaction_type=TransactionType.BUY,
    #         product_type=ProductType.INTRADAY,
    #         order_type=OrderType.MARKET,
    #         validity=Validity.DAY,
    #         tag="testing",
    #         source="API"
    #     )
    # )
    # print("ORDER", order_response.order_number, order_response.message)

# python -m marketfeed_multi_broker_sdk.services.fyers_services
