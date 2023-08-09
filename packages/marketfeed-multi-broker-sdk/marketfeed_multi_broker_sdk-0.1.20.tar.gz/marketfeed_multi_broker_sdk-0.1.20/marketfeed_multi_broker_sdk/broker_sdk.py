from marketfeed_multi_broker_sdk.broker_interface import BrokerInterface
from marketfeed_multi_broker_sdk.brokers.fyers import FYERS
from marketfeed_multi_broker_sdk.brokers.xts import XTS
from marketfeed_multi_broker_sdk.brokers.shoonya import SHOONYA
from marketfeed_multi_broker_sdk.brokers.kotak import KOTAK
from marketfeed_multi_broker_sdk.brokers.kotak_neo import KOTAK_NEO
from marketfeed_multi_broker_sdk.models import Login, Order
from marketfeed_multi_broker_sdk.enums import Broker
# import other brokers as needed


class BrokerSDK:

    def __init__(self, broker: Broker, client_code: str):
        self.broker_name = broker
        self.client_code = client_code

        broker_classes = {
            Broker.FYERS: FYERS,
            Broker.XTS: XTS,
            Broker.SHOONYA: SHOONYA,
            Broker.KOTAK: KOTAK,
            Broker.KOTAK_NEO: KOTAK_NEO,
            # Add more brokers here as you implement them
        }

        if broker in broker_classes:
            self.broker: BrokerInterface = broker_classes[broker](
                client_code)
        else:
            raise ValueError(f"Unsupported broker: {broker}")

    def login(self, login_details: Login):
        return self.broker.login(login_details=login_details)

    def margin(self, token: str):
        return self.broker.margin(token=token)

    def place_order(self, token: str, order_details: Order):
        return self.broker.place_order(token=token, order_details=order_details)

    def holding(self, token: str):
        return self.broker.holding(token=token)

    def position(self, token: str):
        return self.broker.position(token=token)

    def get_transaction_history(self):
        return self.broker.get_transaction_history()
