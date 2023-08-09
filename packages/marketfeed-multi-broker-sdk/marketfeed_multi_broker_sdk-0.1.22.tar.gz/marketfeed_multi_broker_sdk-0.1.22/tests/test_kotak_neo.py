import pytest
from marketfeed_multi_broker_sdk.brokers.kotak_neo import KOTAK_NEO
from marketfeed_multi_broker_sdk.models import Login, LoginResponse, OrderResponse, GetTransactionHistoryResponse, Order, Transaction
from marketfeed_multi_broker_sdk.utils.env_generator import load_env_value

client_code = load_env_value('KOTAK_NEO_CLIENT_CODE')
mobile = load_env_value('KOTAK_NEO_CLIENT_MOBILE')
password = load_env_value('KOTAK_NEO_PASSWORD')
mpin = load_env_value('KOTAK_NEO_MPIN')
consumer_key = load_env_value('KOTAK_NEO_CONSUMER_KEY')
consumer_secret = load_env_value('KOTAK_NEO_CONSUMER_SECRET')


@pytest.fixture
def broker():
    return KOTAK_NEO(client_code=client_code)


def test_login(broker):
    response = broker.login(
        Login(
            mobile=mobile,
            password=password,
            mpin=mpin,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
        )
    )
    assert isinstance(response, LoginResponse)
    assert response.token != None
    assert response.token != ''


# @pytest.mark.parametrize(
#     "order_details, expected_status",
#     [
#         ({"order_id": "1", "product": "Apple",
#          "price": 150.00, "quantity": 10}, 'success'),
#         ({"order_id": "1", "product": "Apple",
#           "price": 150.00, "quantity": 10}, 'success'),
#         # Add more test cases here
#     ],
# )
# def test_place_order(broker, order_details, expected_status):
#     response = broker.place_order(order_details)
#     assert isinstance(response, OrderResponse)
#     assert response.status == expected_status
#     assert isinstance(response.order, Order)


# def test_get_transaction_history(broker):
#     response = broker.get_transaction_history()
#     assert isinstance(response, GetTransactionHistoryResponse)
#     assert response.status == 'success'
#     assert isinstance(response.transactions, list)
#     for transaction in response.transactions:
#         assert isinstance(transaction, Transaction)
