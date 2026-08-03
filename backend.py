# backend.py
import time
import logging
import yfinance as yf
import pandas as pd
import streamlit as st
from config import get_massive_global_universe

# Logging aktivieren, um Fehler in der Konsole zu sehen
logging.basicConfig(level=logging.INFO)

@st.cache_data(ttl=3600)  # Cacht die Daten für 1 Stunde, schont die API-Anfragen
def fetch_screened_data():
    """
    Lädt das Aktien-Universum und holt die Kennzahlen über yfinance ab.
    Enthält Pausen und Fehlerbehandlung für einen stabilen Cloud-Betrieb.
    """
    tickers = get_massive_global_universe()
    data_list = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Wichtige Kennzahlen sicher auslesen (verhindert KeyError, falls Info fehlt)
            data_list.append({
                "Ticker": ticker,
                "Name": info.get("shortName", ticker),
                "Price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "PE": info.get("trailingPE"),
                "PB": info.get("priceToBook"),
                "MarketCap": info.get("marketCap"),
            })
            
            # Kurze Pause, damit Yahoo Finance die Cloud-IP nicht blockiert
            time.sleep(0.1)
            
        except Exception as e:
            logging.warning(f"Fehler beim Laden von {ticker}: {e}")
            continue

    return pd.DataFrame(data_list)

@st.cache_data(ttl=86400)  # Historische Daten für 24 Stunden cachen
def fetch_historical_data(ticker, period="1y"):
    """
    Lädt historische Kursdaten für einen bestimmten Ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        logging.error(f"Fehler beim Laden der historischen Daten für {ticker}: {e}")
        return pd.DataFrame()
