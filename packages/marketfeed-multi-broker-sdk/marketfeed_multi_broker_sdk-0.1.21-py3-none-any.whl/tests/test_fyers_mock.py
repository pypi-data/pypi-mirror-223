# File: tests/test_broker1.py

import pytest
from unittest.mock import Mock
from marketfeed_multi_broker_sdk.brokers.fyers import FYERS
from marketfeed_multi_broker_sdk.models import LoginResponse, Order, OrderResponse, GetTransactionHistoryResponse


def test_login():
    broker1 = FYERS('client_code', 'access_token', 'secret')
    broker1.login = Mock(return_value=LoginResponse(status='success'))
    response = broker1.login()
    assert response.status == 'success'


def test_place_order():
    broker1 = FYERS('client_code', 'access_token', 'secret')
    order = Order(order_id='1234', product='abc', price=100.0, quantity=1)
    broker1.place_order = Mock(
        return_value=OrderResponse(status='success', order=order))
    response = broker1.place_order(order_details={})
    assert response.status == 'success'


def test_get_transaction_history():
    broker1 = FYERS('client_code', 'access_token', 'secret')
    broker1.get_transaction_history = Mock(
        return_value=GetTransactionHistoryResponse(status='success', transactions=[]))
    response = broker1.get_transaction_history()
    assert response.status == 'success'
