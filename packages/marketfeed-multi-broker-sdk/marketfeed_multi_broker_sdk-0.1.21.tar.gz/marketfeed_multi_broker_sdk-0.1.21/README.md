# Multi-Broker SDK

Multi-Broker SDK is a Python library that allows you to seamlessly integrate multiple brokerage services in your application. This package simplifies interaction with different brokers, providing a unified way to implement and manage your trades.

## Installation

Use the package manager pip to install BrokerSDK. Run the following command in your terminal:

```
pip install marketfeed-multi-broker-sdk
pip install git+https://github.com/tradeclone/multi-broker-sdk.git
```

## Usage

To utilize the functionality of BrokerSDK, import it into your Python script:

```
from marketfeed_multi_broker_sdk import BrokerSDK
from marketfeed_multi_broker_sdk import Broker, Login, LoginResponse
```

Initialize the SDK with the specific broker's name and user details:

```
sdk_xts = BrokerSDK(Broker.XTS, client_code='CLIENT_CODE')
sdk_fyers = BrokerSDK(Broker.FYERS, client_code='CLIENT_CODE')
sdk_shoonya = BrokerSDK(Broker.SHOONYA, client_code='CLIENT_CODE')
sdk_kotak_neo = BrokerSDK(Broker.KOTAK_NEO, client_code='CLIENT_CODE')

```

Use the BrokerSDK to log in. The BrokerSDK handles communication with the specific broker based on the provided broker name.

For FYERS:

```
loginResponse: LoginResponse = sdk_fyers.login(
    Login(
        totp_key="TOTP_KEY",
        pin="0000"
    )
)
if loginResponse.token == "":
    print(loginResponse.message)
else:
    print("TOKEN GENERATED", loginResponse.token)
```

For XTS:

```
loginResponse: LoginResponse = sdk_xts.login(
        Login(
            api_key="API_KEY",
            api_secret="API_SECRET"
        )
    )
if loginResponse.token == "":
    print(loginResponse.message)
else:
    print("TOKEN GENERATED", loginResponse.token)
```

For SHOONYA:

```
loginResponse: LoginResponse = sdk_shoonya.login(
        Login(
            password="PASSWORD",
            totp_key="TOTP_KEY",
            app_vendor="APP_VENDOR",
            app_imei="APP_IMEI",
            app_key="APP_KEY"
        )
    )
if loginResponse.token == "":
    print(loginResponse.message)
else:
    print("TOKEN GENERATED", loginResponse.token)
```

For KOTAK_NEO:

```
loginResponse: LoginResponse = sdk_kotak_neo.login(
        Login(
            mobile="MOBILE",
            password="PASSWORD",
            mpin="MPIN",
            consumer_key="CONSUMER_KEY",
            consumer_secret="CONSUMER_SECRET"
        )
    )
if loginResponse.token == "":
    print(loginResponse.message)
else:
    print("TOKEN GENERATED", loginResponse.token)
```

# Contributing

We welcome contributions from the community. If you'd like to contribute to BrokerSDK, feel free to submit a pull request or open an issue on our GitHub page.

Please make sure to update tests as appropriate.

For further details and updates about this project, please read through the documentation on our GitHub page.

Remember, your contributions enhance the capabilities of our project. Happy coding!
