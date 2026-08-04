# backend.py
import pandas as pd
import streamlit as st
import os
import yfinance as yf

@st.cache_data(ttl=3600)
def fetch_screened_data():
    """
    Liest den vorberechneten Datensatz ein und bereinigt Formatierungen.
    """
    snapshot_file = "uni_snapshot.csv"
    
    if os.path.exists(snapshot_file):
        df = pd.read_csv(snapshot_file)
        
        # Sicherheits-Check, falls alte Spaltennamen fehlen
        expected_cols = ["Ticker", "Name", "Price", "P/E (KGV)", "P/B (KBV)", "Umsatz ($B)", "Alpheon Score", "Dividendenrendite (%)"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0.0 if col != "Name" and col != "Ticker" else "N/A"
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
    Lädt historische Kursdaten für den Einzeltitel-Deepdive.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if not hist.empty and "Close" in hist.columns:
            return hist["Close"]
        return hist
    except Exception as e:
        return pd.DataFrame()
