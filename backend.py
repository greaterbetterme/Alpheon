# backend.py
import yfinance as yf
import pandas as pd
import logging
from config import get_massive_global_universe

logging.getLogger('yfinance').setLevel(logging.CRITICAL)

def calculate_alpheon_score(pe, pb, div_yield):
    """Berechnet einen quantitativen Value-Score (0-100) nach Graham-Prinzipien."""
    score = 50
    # KGV Bewertung (günstiger ist besser, ideal zwischen 5 und 15)
    if 0 < pe <= 15:
        score += 25
    elif pe > 25:
        score -= 20
        
    # KBV Bewertung (unter 1.5 ist stark)
    if 0 < pb <= 1.5:
        score += 15
    elif pb > 3.0:
        score -= 15
        
    # Dividendenrendite Bonus
    if div_yield > 2.0:
        score += 10
        
    return max(0, min(100, score))

def fetch_screened_data():
    results = []
    universum = get_massive_global_universe()
    chunk_size = 25
    total = len(universum)
    
    for i in range(0, total, chunk_size):
        chunk = universum[i:i + chunk_size]
        data = yf.Tickers(" ".join(chunk))
        
        for ticker in chunk:
            try:
                stock = data.tickers.get(ticker)
                if not stock:
                    continue
                info = stock.info
                if not info or "marketCap" not in info:
                    continue
                
                raw_div = info.get("dividendYield", 0.0) or 0.0
                # Automatische Korrektur falls Yahoo die Dividende als Ganzzahl/Cent liefert
                if raw_div > 1.0:
                    div_yield = round(raw_div / 100.0 * 100, 2)
                else:
                    div_yield = round(raw_div * 100, 2)
                
                pe = round(info.get("trailingPE", 0.0) or 0.0, 2)
                pb = round(info.get("priceToBook", 0.0) or 0.0, 2)
                
                score = calculate_alpheon_score(pe, pb, div_yield)
                
                results.append({
                    "Ticker": ticker,
                    "Unternehmen": info.get("longName", ticker),
                    "Land": info.get("country", "Unbekannt"),
                    "Alpheon Score": score,
                    "Marktkapitalisierung ($B)": round(info.get("marketCap", 0) / 1e9, 2),
                    "Umsatz ($B)": round(info.get("totalRevenue", 0) / 1e9, 2),
                    "P/E (KGV)": pe,
                    "P/B (KBV)": pb,
                    "Dividendenrendite (%)": div_yield,
                    "Sektor": info.get("sector", "N/A")
                })
            except Exception:
                continue
                
    return pd.DataFrame(results)

def fetch_historical_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        return hist["Close"] if not hist.empty else None
    except Exception:
        return None