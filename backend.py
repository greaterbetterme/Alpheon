# backend.py
import time
import logging
import yfinance as yf
import pandas as pd
import streamlit as st
from config import get_massive_global_universe

logging.basicConfig(level=logging.INFO)

@st.cache_data(ttl=3600)
def fetch_screened_data():
    tickers = get_massive_global_universe()
    data_list = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            score = 50  # Fallback für den Score
            market_cap = info.get("marketCap", 0)
            market_cap_b = market_cap / 1e9 if market_cap else 0
            
            # Dividendenrendite von yfinance holen (wird oft als Dezimalzahl geliefert, z.B. 0.02 = 2%)
            dividend_yield = info.get("dividendYield", 0)
            dividend_pct = (dividend_yield * 100) if dividend_yield else 0.0

            data_list.append({
                "Ticker": ticker,
                "Name": info.get("shortName", ticker),
                "Price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
                "P/E (KGV)": info.get("trailingPE", 0) or 0,
                "P/B (KBV)": info.get("priceToBook", 0) or 0,
                "Umsatz ($B)": market_cap_b,
                "Alpheon Score": score,
                "Dividendenrendite (%)": dividend_pct
            })
            
            time.sleep(0.5)
            
        except Exception as e:
            logging.warning(f"Fehler beim Laden von {ticker}: {e}")
            continue

    df = pd.DataFrame(data_list)
    
    # Sicherheitsnetz mit allen benötigten Spalten inklusive Dividendenrendite
    if df.empty:
        df = pd.DataFrame(columns=[
            "Ticker", "Name", "Price", "P/E (KGV)", "P/B (KBV)", 
            "Umsatz ($B)", "Alpheon Score", "Dividendenrendite (%)"
        ])
        
    return df

@st.cache_data(ttl=86400)
def fetch_historical_data(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period)
    except Exception as e:
        logging.error(f"Fehler bei historischen Daten für {ticker}: {e}")
        return pd.DataFrame()
