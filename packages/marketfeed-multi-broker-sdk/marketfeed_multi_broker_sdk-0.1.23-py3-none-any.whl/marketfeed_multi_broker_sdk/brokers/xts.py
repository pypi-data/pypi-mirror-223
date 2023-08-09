from typing import Any, Dict
from marketfeed_multi_broker_sdk.broker_interface import BrokerInterface
from marketfeed_multi_broker_sdk.models import Login, LoginResponse, MarginResponse, Order, OrderResponse, HoldingResponse, PositionResponse, GetTransactionHistoryResponse
from marketfeed_multi_broker_sdk.services.xts_services import XtsAPIServices


class XTS(BrokerInterface):

    def login(self, login_details: Login):
        xts_api_service = XtsAPIServices()
        token, message = xts_api_service.XtsLogin(
            client_code=self.client_code,
            login_details=login_details
        )
        return LoginResponse(token=token, message=message)

    def margin(self, token) -> MarginResponse:
        xts_api_service = XtsAPIServices()
        margin_response: MarginResponse = xts_api_service.XtsMargin(
            token=token,
            client_code=self.client_code,
        )
        return margin_response

    def place_order(self, token, order_details: Order) -> OrderResponse:
        xts_api_service = XtsAPIServices()
        order_response: OrderResponse = xts_api_service.XtsPlaceOrder(
            token=token,
            client_code=self.client_code,
            order_details=order_details
        )
        return order_response

    def holding(self, token) -> HoldingResponse:
        xts_api_service = XtsAPIServices()
        holding_response: HoldingResponse = xts_api_service.XtsHolding(
            token=token,
            client_code=self.client_code,
        )
        return holding_response

    def position(self, token) -> PositionResponse:
        xts_api_service = XtsAPIServices()
        position_response: PositionResponse = xts_api_service.XtsPosition(
            token=token,
            client_code=self.client_code,
        )
        return position_response

    def get_transaction_history(self) -> GetTransactionHistoryResponse:
        # Replace with actual implementation for getting transaction history from xts
        print(
            f"Getting transaction history for xts client {self.client_code}")
        # This is just a placeholder and should be replaced with actual transactions
        transactions = []
        return GetTransactionHistoryResponse(status='success', transactions=transactions)
