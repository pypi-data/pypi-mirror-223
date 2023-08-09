import requests
import json
from urllib.parse import urlparse
from marketfeed_multi_broker_sdk.models import Login, MarginData, MarginResponse, Order, OrderResponse, HoldingData, HoldingResponse, PositionData, PositionResponse
from marketfeed_multi_broker_sdk.enums import Broker, Exchange, TransactionType, ProductType, OrderType, Validity


class _XtsAPIService:
    _BASE_URL = "https://ttblaze.iifl.com/interactive"
    _SUCCESS = 1
    _ERROR = -1

    def _start_session(self, api_key, api_secret):
        try:
            print(api_key, api_secret)
            session_response = requests.post(
                f'{self._BASE_URL}/user/session',
                headers={
                    'Content-Type': 'application/json',
                },
                json={
                    'secretKey': api_secret,
                    'appKey': api_key,
                    'source': 'WebAPI'
                }
            )
            host_lookup_response_json = json.loads(session_response.text)
            if session_response.status_code != 200:
                return [self._ERROR, host_lookup_response_json['description']]
            if host_lookup_response_json['type'] == 'error':
                return [self._ERROR, host_lookup_response_json['description']]

            token = host_lookup_response_json['result']['token']
            return [self._SUCCESS, token]
        except Exception as e:
            return [self._ERROR, e]

    def _margin(self, token, client_code):
        try:
            margin_response = requests.get(
                f'{self._BASE_URL}/user/balance?clientID={client_code}',
                headers={
                    'Content-Type': 'application/json',
                    "Authorization": token,
                },
            )
            margin_response_json = json.loads(margin_response.text)
            if margin_response.status_code != 200:
                return [self._ERROR, margin_response_json['description']]

            if margin_response_json['type'] == 'error':
                return [self._ERROR, margin_response_json['description']]

            balance_list = margin_response_json['result']['BalanceList'][0]['limitObject']['RMSSubLimits']
            margin_data: MarginData = MarginData(
                available_balance=float(balance_list['cashAvailable']),
                utilized_balance=float(balance_list['marginUtilized']),
                remaining_balance=float(balance_list['netMarginAvailable'])
            )
            return [self._SUCCESS, margin_data]
        except Exception as e:
            return [self._ERROR, e]

    def _place_order(self, token, client_code, exchange, symbol, quantity, price, trigger_price, disclosed_quantity, product_type, transaction_type, order_type, validity, tag, ordersource):
        try:
            url = f'{self._BASE_URL}/orders'
            headers = {
                'Content-Type': 'application/json',
                "Authorization": token,
            }
            payload = {
                "exchangeSegment": exchange,
                "exchangeInstrumentID": symbol,
                "productType": product_type,
                "orderType": order_type,
                "orderSide": transaction_type,
                "timeInForce": validity,
                "disclosedQuantity": disclosed_quantity,
                "orderQuantity": quantity,
                "limitPrice": price,
                "stopPrice": 0,
                "orderUniqueIdentifier": tag,
            }
            response = requests.request(
                "POST", url, headers=headers, json=payload)
            response_json = json.loads(response.text)
            if response.status_code != 200:
                return [self._ERROR, response_json['description']]

            if response_json['type'] == 'error':
                return [self._ERROR, response_json['description']]

            order_no = response_json['result']['AppOrderID']
            return [self._SUCCESS, order_no]
        except Exception as e:
            return [self._ERROR, e]

    def _holding(self, token, client_code):
        try:
            response = requests.get(
                f'{self._BASE_URL}/portfolio/holdings?clientID={client_code}',
                headers={
                    'Content-Type': 'application/json',
                    "Authorization": token,
                },
            )
            if response.status_code != 200:
                return [self._ERROR, response.text]
            response_json = json.loads(response.text)

            if response_json['type'] == 'error':
                return [self._ERROR, response_json['description']]

            holdings_data = response_json['result']['RMSHoldings']['Holdings']
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
            response = requests.get(
                f'{self._BASE_URL}/portfolio/positions?clientID={client_code}&dayOrNet=NetWise',
                headers={
                    'Content-Type': 'application/json',
                    "Authorization": token,
                },
            )
            if response.status_code != 200:
                return [self._ERROR, response.text]
            response_json = json.loads(response.text)

            if response_json['type'] == 'error':
                return [self._ERROR, response_json['description']]

            positions_data = response_json['result']['positionList']
            positions_list = []
            for value in positions_data:
                position_data: PositionData = PositionData(
                    symbol=value['TradingSymbol'],
                    symbol_token=str(value['ExchangeInstrumentId']),
                    quantity=abs(int(value['Quantity'])),
                    transaction_type="BUY" if int(
                        value['Quantity']) > 0 else "SELL",
                    buy_average=float(value['BuyAveragePrice']),
                    sell_average=float(value['SellAveragePrice'])
                )
                positions_list.append(position_data)
            return [self._SUCCESS, positions_list]
        except Exception as e:
            return [self._ERROR, e]


class XtsAPIServices(_XtsAPIService):
    _BROKER = Broker.XTS

    def XtsLogin(self, client_code, login_details: Login):

        start_session_response = super()._start_session(
            api_key=login_details.api_key, api_secret=login_details.api_secret)
        if start_session_response[0] != super()._SUCCESS:
            return ["", f"{client_code} start session failure - {start_session_response[1]}"]
        return [start_session_response[1], "success"]

    def XtsMargin(self, token, client_code) -> MarginResponse:
        start_session_response = super()._margin(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return MarginResponse(
                margin=None,
                message=f"{client_code} start session failure - {start_session_response[1]}"
            )
        return MarginResponse(margin=start_session_response[1], message="success")

    def XtsPlaceOrder(self, token, client_code, order_details: Order) -> OrderResponse:
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

    def XtsHolding(self, token, client_code) -> HoldingResponse:
        start_session_response = super()._holding(
            token=token,
            client_code=client_code)
        if start_session_response[0] != super()._SUCCESS:
            return HoldingResponse(
                holding=None,
                message=f"{client_code} start session failure - {start_session_response[1]}"
            )
        return HoldingResponse(holding=start_session_response[1], message="success")

    def XtsPosition(self, token, client_code) -> PositionResponse:
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
#     client_code = load_env_value('XTS_CLIENT_CODE')
#     api_key = load_env_value('XTS_API_KEY')
#     api_secret = load_env_value('XTS_API_SECRET')

#     xtsAPI = XtsAPIServices()
#     token, message = xtsAPI.XtsLogin(
#         client_code=client_code,
#         login_details=Login(
#             api_key=api_key,
#             api_secret=api_secret,
#         )
#     )
#     print("TOKEN", token, message)
#     margin_response: MarginResponse = xtsAPI.XtsMargin(
#         token=token, client_code=client_code)
#     print("MARGIN", margin_response.margin, margin_response.message)

    # holding_response: HoldingResponse = xtsAPI.XtsHolding(
    #     token=token, client_code=client_code)
    # print("HOLDING", holding_response.holding, holding_response.message)

    # holding_response: PositionResponse = xtsAPI.XtsPosition(
    #     token=token, client_code=client_code)
    # print("POSITION", holding_response.position, holding_response.message)

    # order_response: OrderResponse = xtsAPI.XtsPlaceOrder(
    #     token=token,
    #     client_code=client_code,
    #     order_details=Order(
    #         exchange=Exchange.NSECM,
    #         symbol="3045",
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

# python3 -m marketfeed_multi_broker_sdk.services.xts_services
