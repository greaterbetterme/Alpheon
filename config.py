# config.py
import streamlit as st

@st.cache_data(ttl=86400)
def get_massive_global_universe():
    us_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "BRK-B", "TSLA", "UNH", "JNJ", 
        "XOM", "JPM", "V", "PG", "MA", "HD", "CVX", "MRK", "ABBV", "PEP", "KO", "BAC", 
        "COST", "ADBE", "WMT", "MCD", "CSCO", "PFE", "TMO", "ACN", "ABT", "LIN", "DIS", 
        "DHR", "NFLX", "VZ", "INTC", "CMCSA", "NKE", "AMD", "IBM", "QCOM", "CAT", "GE",
        "AMGN", "SPGI", "HON", "LOW", "NOW", "RTX", "GS", "BA", "DE", "BLK", "UBER",
        "LLY", "ORCL", "CRM", "AXP", "TMUS", "ISRG", "BKNG", "TJX", "MDT", "NEE", "PGR",
        "LRCX", "ADI", "MDLZ", "GILD", "VRTX", "CB", "MMC", "PANW", "SNPS", "REGN",
        "SO", "DUK", "CI", "ITW", "SHW", "CL", "APD", "NSC", "ZTS", "CSX", "SLB",
        "USB", "TGT", "PNC", "NOC", "EQIX", "BDX", "BSX", "HUM", "MU", "ICE", "WM",
        "ETN", "CDNS", "MO", "ORLY", "CLX", "GIS", "HSY", "KMB", "SYK", "PSA", "O",
        "F", "GM", "INTC", "HPQ", "EBAY", "K", "AAL", "DAL", "UAL", "CCL", "RCL"
    ]
    for prefix in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
        us_tickers.append(f"{prefix}T")

    eu_tickers = [
        "SIE.DE", "SAP.DE", "ALV.DE", "DTE.DE", "AIR.DE", "MUV2.DE", "BAS.DE", "DB1.DE", 
        "DHL.DE", "BMW.DE", "MBG.DE", "VOW3.DE", "ENR.DE", "RWE.DE", "EOAN.DE", "IFX.DE",
        "HEI.DE", "SHL.DE", "BEI.DE", "HEN3.DE", "CON.DE", "ZAL.DE", "BNR.DE", "PAH3.DE",
        "MC.PA", "OR.PA", "TTE.PA", "SAN.PA", "SU.PA", "BN.PA", "KER.PA", "SAF.PA", "AIR.PA",
        "NESN.SW", "ROG.SW", "NOVN.SW", "ZURN.SW", "ABBN.SW", "SHEL.L", "AZN.L", "HSBA.L",
        "BP.L", "GSK.L", "RIO.L", "ULVR.L", "DGE.L", "BARC.L", "LLOY.L", "VOD.L"
    ]

    asia_au_tickers = [
        "7203.T", "6758.T", "9984.T", "9432.T", "8306.T", "4063.T", "6501.T", "8035.T",
        "6861.T", "6902.T", "7974.T", "4502.T", "4503.T", "8001.T", "8031.T", "9433.T",
        "TSM", "2330.TW", "005930.KS", "000660.KS", "BHP.AX", "CBA.AX", "CSL.AX", 
        "NAB.AX", "WBC.AX", "ANZ.AX", "MQG.AX", "WES.AX", "FMG.AX", "TLS.AX"
    ]
    
    return list(set(us_tickers + eu_tickers + asia_au_tickers))