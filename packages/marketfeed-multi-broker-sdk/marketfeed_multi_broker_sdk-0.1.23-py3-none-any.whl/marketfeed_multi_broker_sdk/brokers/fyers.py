from typing import Any, Dict
from marketfeed_multi_broker_sdk.broker_interface import BrokerInterface
from marketfeed_multi_broker_sdk.models import Login, MarginResponse, Order, LoginResponse, OrderResponse, HoldingResponse, PositionResponse, GetTransactionHistoryResponse
from marketfeed_multi_broker_sdk.services.fyers_services import FyersAPIServices


class FYERS(BrokerInterface):

    def login(self, login_details: Login):
        fyers_api_service = FyersAPIServices()
        token, message = fyers_api_service.FyersLogin(
            client_code=self.client_code,
            login_details=login_details
        )
        return LoginResponse(token=token, message=message)

    def margin(self, token) -> MarginResponse:
        fyers_api_service = FyersAPIServices()
        margin_response: MarginResponse = fyers_api_service.FyersMargin(
            token=token,
            client_code=self.client_code,
        )
        return margin_response

    def place_order(self, token, order_details: Order) -> OrderResponse:
        fyers_api_service = FyersAPIServices()
        order_response: OrderResponse = fyers_api_service.FyersPlaceOrder(
            token=token,
            client_code=self.client_code,
            order_details=order_details
        )
        return order_response

    def holding(self, token) -> HoldingResponse:
        fyers_api_service = FyersAPIServices()
        holding_response: HoldingResponse = fyers_api_service.FyersHolding(
            token=token,
            client_code=self.client_code,
        )
        return holding_response

    def position(self, token) -> PositionResponse:
        fyers_api_service = FyersAPIServices()
        position_response: PositionResponse = fyers_api_service.FyersPosition(
            token=token,
            client_code=self.client_code,
        )
        return position_response

    def get_transaction_history(self) -> GetTransactionHistoryResponse:
        # Replace with actual implementation for getting transaction history from fyers
        print(
            f"Getting transaction history for fyers client {self.client_code}")
        # This is just a placeholder and should be replaced with actual transactions
        transactions = []
        return GetTransactionHistoryResponse(status='success', transactions=transactions)
