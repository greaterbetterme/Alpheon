# backend.py
import pandas as pd
import streamlit as st
import os

@st.cache_data(ttl=3600)
def fetch_screened_data():
    """
    Liest den vorberechneten Datensatz ein.
    """
    snapshot_file = "uni_snapshot.csv"
    
    if os.path.exists(snapshot_file):
        df = pd.read_csv(snapshot_file)
    else:
        # Fallback, falls die CSV noch nicht existiert
        df = pd.DataFrame(columns=[
            "Ticker", "Name", "Price", "P/E (KGV)", "P/B (KBV)", 
            "Umsatz ($B)", "Alpheon Score", "Dividendenrendite (%)"
        ])
        
    return df

@st.cache_data(ttl=86400)
def fetch_historical_data(ticker, period="1y"):
    """
    Historische Daten können bei Bedarf weiterhin live geladen werden 
    (da es nur ein einzelner Ticker bei Klick ist, gibt das fast nie Rate-Limits).
    """
    try:
        stock = yf.Ticker(ticker) if 'yf' in globals() else None
        # Falls yfinance hier direkt benötigt wird:
        import yfinance as yf
        return yf.Ticker(ticker).history(period=period)
    except Exception as e:
        return pd.DataFrame()
