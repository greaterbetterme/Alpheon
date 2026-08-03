# update_data.py
import time
import pandas as pd
import yfinance as yf
from config import get_massive_global_universe

def generate_snapshot():
    tickers = get_massive_global_universe()
    data_list = []

    print(f"Starte Daten-Update für {len(tickers)} Ticker...")

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            score = 50  # Dein Alpheon Score (hier deine Logik einbauen)
            market_cap = info.get("marketCap", 0)
            market_cap_b = market_cap / 1e9 if market_cap else 0
            
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
            
            # Kurze Pause für den lokalen/GitHub-Abruf
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Fehler bei {ticker}: {e}")
            continue

    df = pd.DataFrame(data_list)
    
    # Als CSV speichern, die deine App später einliest
    df.to_csv("uni_snapshot.csv", index=False)
    print("Snapshot erfolgreich als uni_snapshot.csv gespeichert!")

if __name__ == "__main__":
    generate_snapshot()
