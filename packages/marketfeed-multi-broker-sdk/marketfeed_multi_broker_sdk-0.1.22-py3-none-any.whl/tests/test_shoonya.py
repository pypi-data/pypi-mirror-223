import pytest
from marketfeed_multi_broker_sdk.brokers.shoonya import SHOONYA
from marketfeed_multi_broker_sdk.models import Login, LoginResponse, OrderResponse, GetTransactionHistoryResponse, Order, Transaction
from marketfeed_multi_broker_sdk.utils.env_generator import load_env_value

client_code = load_env_value('SHOONYA_CLIENT_CODE')
password = load_env_value('SHOONYA_PASSWORD')
totp_key = load_env_value('SHOONYA_TOTP_KEY')
app_vendor = load_env_value('SHOONYA_APP_VENDOR')
app_imei = load_env_value('SHOONYA_APP_IMEI')
app_key = load_env_value('SHOONYA_APP_KEY')


@pytest.fixture
def broker():
    return SHOONYA(client_code=client_code)


def test_login(broker):
    response = broker.login(
        Login(
            password=password,
            totp_key=totp_key,
            app_vendor=app_vendor,
            app_imei=app_imei,
            app_key=app_key
        )
    )
    assert isinstance(response, LoginResponse)
    assert response.token != None
    assert response.token != ''


@pytest.mark.parametrize(
    "order_details, expected_status",
    [
        ({"order_id": "1", "product": "Apple",
         "price": 150.00, "quantity": 10}, 'success'),
        ({"order_id": "1", "product": "Apple",
          "price": 150.00, "quantity": 10}, 'success'),
        # Add more test cases here
    ],
)
def test_place_order(broker, order_details, expected_status):
    response = broker.place_order(order_details)
    assert isinstance(response, OrderResponse)
    assert response.status == expected_status
    assert isinstance(response.order, Order)


def test_get_transaction_history(broker):
    response = broker.get_transaction_history()
    assert isinstance(response, GetTransactionHistoryResponse)
    assert response.status == 'success'
    assert isinstance(response.transactions, list)
    for transaction in response.transactions:
        assert isinstance(transaction, Transaction)
