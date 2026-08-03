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
            
            # Beispiel für die Berechnung/Auslesung des Alpheon Scores (an deine Logik anpassen)
            # Falls du eine eigene Berechnungsfunktion hast, füge sie hier ein.
            score = 50  # Fallback-Wert, falls keine Metrik berechnet wird
            
            market_cap = info.get("marketCap", 0)
            market_cap_b = market_cap / 1e9 if market_cap else 0 # Umrechnung in Milliarden

            data_list.append({
                "Ticker": ticker,
                "Name": info.get("shortName", ticker),
                "Price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
                "P/E (KGV)": info.get("trailingPE", 0) or 0,
                "P/B (KBV)": info.get("priceToBook", 0) or 0,
                "Umsatz ($B)": market_cap_b, # Entspricht dem Spaltennamen im Filter
                "Alpheon Score": score
            })
            
            # WICHTIG: Längere Pause, damit Yahoo Cloud-IPs nicht sperrt
            time.sleep(0.5)
            
        except Exception as e:
            logging.warning(f"Fehler beim Laden von {ticker}: {e}")
            continue

    df = pd.DataFrame(data_list)
    
    # Sicherheitsnetz: Falls der DataFrame komplett leer ist, leere Spalten mit den exakten Namen erzeugen,
    # damit die App wegen fehlender Keys nicht abstürzt.
    if df.empty:
        df = pd.DataFrame(columns=["Ticker", "Name", "Price", "P/E (KGV)", "P/B (KBV)", "Umsatz ($B)", "Alpheon Score"])
        
    return df

@st.cache_data(ttl=86400)
def fetch_historical_data(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period)
    except Exception as e:
        logging.error(f"Fehler bei historischen Daten für {ticker}: {e}")
        return pd.DataFrame()
