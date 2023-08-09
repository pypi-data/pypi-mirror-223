# File: marketfeed_multi_broker_sdk/models.py
from marketfeed_multi_broker_sdk.enums import Exchange, TransactionType, ProductType, OrderType, Validity

from pydantic import BaseModel
from typing import List, Optional


class Login(BaseModel):
    password: Optional[str] = ""
    totp_key: Optional[str] = ""
    pin: Optional[str] = ""
    mobile: Optional[str] = ""
    mpin: Optional[str] = ""
    api_key: Optional[str] = ""
    api_secret: Optional[str] = ""
    app_vendor: Optional[str] = ""
    app_imei: Optional[str] = ""
    app_key: Optional[str] = ""
    consumer_key: Optional[str] = ""
    consumer_secret: Optional[str] = ""


class LoginResponse(BaseModel):
    token: str
    message: str


class MarginData(BaseModel):
    available_balance: float
    utilized_balance: float
    remaining_balance: float


class MarginResponse(BaseModel):
    margin: Optional[MarginData] = None
    message: Optional[str] = None


class HoldingData(BaseModel):
    symbol: Optional[str] = None
    symbol_token: Optional[str] = None
    quantity: int
    average_price: float


class HoldingResponse(BaseModel):
    holding: Optional[List[HoldingData]] = None
    message: Optional[str] = None


class PositionData(BaseModel):
    symbol: Optional[str] = None
    symbol_token: Optional[str] = None
    quantity: int
    transaction_type: str
    buy_average: float
    sell_average: float


class PositionResponse(BaseModel):
    position: Optional[List[PositionData]] = None
    message: Optional[str] = None


class Order(BaseModel):
    exchange: Exchange  # NSE / NFO / CDS / MCX / BSE
    symbol: str  # RELIANCE-EQ, TATAMOTORS-EQ
    quantity: int
    price: float
    trigger_price: float
    disclosed_quantity: int
    transaction_type: TransactionType
    product_type: ProductType  # CNC, NRML,  MIS, BRACKET ORDER, COVER ORDER
    order_type: OrderType  # Limit, Market, SL-M, SL-L
    validity: Validity  # DAY / EOS / IOC
    tag: str
    source: str
    # Add more fields as needed...


class OrderResponse(BaseModel):
    order_number: str
    message: Optional[str] = None


class Transaction(BaseModel):
    transaction_id: str
    order_id: str
    amount: float
    date: str
    # Add more fields as needed...


class GetTransactionHistoryResponse(BaseModel):
    status: str
    transactions: List[Transaction]
    message: Optional[str] = None
