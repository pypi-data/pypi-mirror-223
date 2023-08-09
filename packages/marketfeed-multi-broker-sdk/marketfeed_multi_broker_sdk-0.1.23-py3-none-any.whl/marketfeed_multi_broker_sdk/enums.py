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
    MCX = "MCX"


class Segment(Enum):
    CASH_MARKET = "CM"  # CASH MARKET
    FUTURES_AND_OPTIONS = "FO"  # FUTURES AND OPTIONS
    CURRENCY_DERIVATIVES = "CD"  # CURRENCY DERIVATIVES


class ExchangeSegment(Enum):
    NSE_CM: {
        Broker.FYERS: "NSE",
        Broker.XTS: "NSECM",
        Broker.SHOONYA: "NSE",
        Broker.KOTAK_NEO: "nse_cm",
    }
    NSE_FO: {
        Broker.FYERS: "NSE",
        Broker.XTS: "NSEFO",
        Broker.SHOONYA: "NFO",
        Broker.KOTAK_NEO: "nse_fo",
    }
    NSE_CD: {
        Broker.FYERS: "NSE",
        Broker.XTS: "NSECD",
        Broker.SHOONYA: "CDS",
        Broker.KOTAK_NEO: "nse_cd",
    }
    BSE_CM: {
        Broker.FYERS: "BSE",
        Broker.XTS: "BSECM",
        Broker.SHOONYA: "BSE",
        Broker.KOTAK_NEO: "bse_cm",
    }
    BSE_FO: {
        Broker.FYERS: "BSE",
        Broker.XTS: "BSEFO",
        Broker.SHOONYA: "BFO",
        Broker.KOTAK_NEO: "bse_fo",
    }
    MCX_FO: {
        Broker.FYERS: "MCX",
        Broker.XTS: "MCXFO",
        Broker.SHOONYA: "MCX",
        Broker.KOTAK_NEO: "mcx_fo",
    }


class TransactionType(Enum):
    BUY = {
        Broker.FYERS: 1,
        Broker.XTS: "BUY",
        Broker.SHOONYA: "B",
        Broker.KOTAK: "BUY",
        Broker.KOTAK_NEO: "B",
    }
    SELL = {
        Broker.FYERS: -1,
        Broker.XTS: "SELL",
        Broker.SHOONYA: "S",
        Broker.KOTAK: "SELL",
        Broker.KOTAK_NEO: "S",
    }


class ProductType(Enum):
    CNC = {
        Broker.FYERS: "CNC",
        Broker.XTS: "CNC",
        Broker.SHOONYA: "C",
        Broker.KOTAK_NEO: "CNC",
    }
    INTRADAY = {
        Broker.FYERS: "INTRADAY",
        Broker.XTS: "MIS",
        Broker.SHOONYA: "I",
        Broker.KOTAK_NEO: "MIS",
    }
    NRML = {
        Broker.FYERS: "MARGIN",
        Broker.XTS: "NRML",
        Broker.SHOONYA: "M",
        Broker.KOTAK_NEO: "NRML",
    }
    BRACKET_ORDER = {
        Broker.FYERS: "BO",
        Broker.XTS: "",
        Broker.SHOONYA: "B",
        Broker.KOTAK_NEO: "BO",
    }
    COVER_ORDER = {
        Broker.FYERS: "CO",
        Broker.XTS: "",
        Broker.SHOONYA: "H",
        Broker.KOTAK_NEO: "CO",
    }


class OrderType(Enum):
    LIMIT = {
        Broker.FYERS: 1,
        Broker.XTS: "LIMIT",
        Broker.SHOONYA: "LMT",
        Broker.KOTAK_NEO: "L",
    }
    MARKET = {
        Broker.FYERS: 2,
        Broker.XTS: "MARKET",
        Broker.SHOONYA: "MKT",
        Broker.KOTAK_NEO: "MKT",
    }
    SL_M = {
        Broker.FYERS: 3,
        Broker.XTS: "STOPMARKET",
        Broker.SHOONYA: "SL-MKT",
        Broker.KOTAK_NEO: "SL-M",
    }
    SL_L = {
        Broker.FYERS: 4,
        Broker.XTS: "STOPLIMIT",
        Broker.SHOONYA: "SL-LMT",
        Broker.KOTAK_NEO: "SL",
    }


class Validity(Enum):
    DAY = {
        Broker.FYERS: "DAY",
        Broker.XTS: "DAY",
        Broker.SHOONYA: "DAY",
        Broker.KOTAK_NEO: "DAY"
    }
    IOC = {
        Broker.FYERS: "IOC",
        Broker.XTS: "IOC",
        Broker.SHOONYA: "IOC",
        Broker.KOTAK_NEO: "IOC"
    }
