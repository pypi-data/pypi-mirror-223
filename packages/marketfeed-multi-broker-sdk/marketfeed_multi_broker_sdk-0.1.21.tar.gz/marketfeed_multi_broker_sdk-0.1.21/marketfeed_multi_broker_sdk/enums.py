from enum import Enum


class Broker(Enum):
    SHOONYA = "shoonya"
    FYERS = "fyers"
    XTS = "xts"
    KOTAK = "kotak"
    KOTAK_NEO = "kotak_neo"
    # You can add more brokers here as needed...


class Exchange(Enum):
    NSE = "NSE"
    BSE = "BSE"
    # CDS = "CDS"
    # MCX = "MCX"


class Segment(Enum):
    CASH = "CASH"
    DERIVATIVE = "DERIVATIVE"
    # COMMODITY = "COMMODITY"
    # CURRENCY ="CURRENCY"


class ExchangeSegment(Enum):
    NSE_CASH: {
        Broker.FYERS: "NSE:",
        Broker.KOTAK_NEO: "nse_cm",
    }
    BSE_CASH: {
        Broker.KOTAK_NEO: "bse_cm",
    }
    NSE_DERIVATIVE: {
        Broker.KOTAK_NEO: "nse_fo",
    }
    BSE_DERIVATIVE: {
        Broker.KOTAK_NEO: "nse_fo",
    }


class TransactionType(Enum):
    BUY = {
        Broker.SHOONYA: "B",
        Broker.FYERS: 1,
        Broker.XTS: "BUY",
        Broker.KOTAK: "BUY",
        Broker.KOTAK_NEO: "B",
    }
    SELL = {
        Broker.SHOONYA: "S",
        Broker.FYERS: -1,
        Broker.XTS: "SELL",
        Broker.KOTAK: "SELL",
        Broker.KOTAK_NEO: "S",
    }


class ProductType(Enum):
    CNC = {
        Broker.SHOONYA: "C",
        Broker.FYERS: "CNC",
        Broker.XTS: "",
        Broker.KOTAK_NEO: "CNC",
    }
    NRML = {
        Broker.SHOONYA: "M",
        Broker.FYERS: "MARGIN",
        Broker.XTS: "NRML",
        Broker.KOTAK_NEO: "NRML",
    }
    INTRADAY = {
        Broker.SHOONYA: "I",
        Broker.FYERS: "INTRADAY",
        Broker.XTS: "INTRADAY",
        Broker.KOTAK_NEO: "INTRADAY",
    }
    MIS = {
        Broker.SHOONYA: "I",
        Broker.FYERS: "MARGIN",
        Broker.XTS: "MIS",
        Broker.KOTAK_NEO: "MIS",
    }
    BRACKET_ORDER = {
        Broker.SHOONYA: "B",
        Broker.FYERS: "BO",
        Broker.XTS: "",
        Broker.KOTAK_NEO: "BO",
    }
    COVER_ORDER = {
        Broker.SHOONYA: "H",
        Broker.FYERS: "CO",
        Broker.XTS: "",
        Broker.KOTAK_NEO: "CO",
    }


class OrderType(Enum):
    LIMIT = {
        Broker.SHOONYA: "LMT",
        Broker.FYERS: 1,
        Broker.XTS: "LIMIT",
        Broker.KOTAK_NEO: "L",
    }
    MARKET = {
        Broker.SHOONYA: "MKT",
        Broker.FYERS: 2,
        Broker.XTS: "MARKET",
        Broker.KOTAK_NEO: "MKT",
    }
    SLM = {
        Broker.SHOONYA: "SL-MKT",
        Broker.FYERS: 3,
        Broker.XTS: "STOPMARKET",
        Broker.KOTAK_NEO: "SL-M",
    }
    SLL = {
        Broker.SHOONYA: "SL-LMT",
        Broker.FYERS: 4,
        Broker.XTS: "STOPLIMIT",
        Broker.KOTAK_NEO: "SL",
    }


class Validity(Enum):
    DAY = {
        Broker.SHOONYA: "DAY",
        Broker.FYERS: "DAY",
        Broker.XTS: "DAY",
        Broker.KOTAK_NEO: "DAY"
    }
    IOC = {
        Broker.SHOONYA: "IOC",
        Broker.FYERS: "IOC",
        Broker.XTS: "IOC",
        Broker.KOTAK_NEO: "IOC"
    }
