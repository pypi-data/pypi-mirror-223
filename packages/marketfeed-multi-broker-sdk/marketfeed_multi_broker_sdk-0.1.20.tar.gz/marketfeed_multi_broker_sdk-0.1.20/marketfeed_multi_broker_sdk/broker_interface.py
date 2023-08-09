# File: marketfeed_multi_broker_sdk/broker_interface.py

from abc import ABC, abstractmethod
from typing import Any, Dict
from marketfeed_multi_broker_sdk.models import Login, MarginResponse, Order, LoginResponse, OrderResponse, HoldingResponse, PositionResponse, GetTransactionHistoryResponse


class BrokerInterface(ABC):
    def __init__(self, client_code: str) -> None:
        self.client_code = client_code
        self.token = None

    @abstractmethod
    def login(self, login_details: Login) -> LoginResponse:
        pass

    @abstractmethod
    def margin(self, token: str) -> MarginResponse:
        return self.broker.margin(token=token)

    @abstractmethod
    def place_order(self, token: str, order_details: Order) -> OrderResponse:
        pass

    @abstractmethod
    def holding(self, token: str) -> HoldingResponse:
        return self.broker.holding(token=token)

    @abstractmethod
    def position(self, token: str) -> PositionResponse:
        return self.broker.position(token=token)

    @abstractmethod
    def get_transaction_history(self) -> GetTransactionHistoryResponse:
        pass
