# update_data.py
import time
import pandas as pd
import yfinance as yf
from config import get_massive_global_universe

def calculate_alpheon_score(pe, pb, div_yield):
    """
    Berechnet einen echten Value-Score von 0 bis 100 basierend auf Graham/Buffett Kriterien:
    - Gutes KGV (unter 20 ist top, unter 15 exzellent)
    - Gutes KBV (unter 3 ist gut)
    - Dividendenrendite vorhanden
    """
    score = 50.0  # Startpunkt

    # KGV (P/E) Bewertung
    if pe and pe > 0:
        if pe < 10:
            score += 25
        elif pe < 15:
            score += 15
        elif pe < 25:
            score += 5
        elif pe > 40:
            score -= 20  # Teuer / Überbewertet

    # KBV (P/B) Bewertung
    if pb and pb > 0:
        if pb < 1.5:
            score += 20
        elif pb < 3.0:
            score += 10
        elif pb > 6.0:
            score -= 15

    # Dividenden-Bonus
    if div_yield and div_yield > 0:
        score += 5

    # Begrenzen auf Skala von 0 bis 100
    return max(0.0, min(100.0, round(score, 1)))

def generate_snapshot():
    tickers = get_massive_global_universe()
    data_list = []

    print(f"Starte Daten-Update für {len(tickers)} Ticker...")

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            pe = info.get("trailingPE") or 0
            pb = info.get("priceToBook") or 0
            
            market_cap = info.get("marketCap", 0)
            market_cap_b = market_cap / 1e9 if market_cap else 0
            
            # Yahoo liefert dividendYield manchmal als Dezimal (0.025 = 2.5%) 
            # oder manchmal bereits als Prozent oder None
            div_raw = info.get("dividendYield")
            if div_raw is not None:
                # Falls es kleiner als 1 ist, ist es eine Dezimalzahl (z.B. 0.03 = 3%)
                if div_raw < 1.0:
                    dividend_pct = div_raw * 100
                else:
                    dividend_pct = div_raw # Falls es schon im Prozentformat ist
            else:
                dividend_pct = 0.0

            # Echten Alpheon Score berechnen
            score = calculate_alpheon_score(pe, pb, div_raw)

            data_list.append({
                "Ticker": ticker,
                "Name": info.get("shortName", ticker),
                "Price": info.get("currentPrice") or info.get("regularMarketPrice", 0),
                "P/E (KGV)": pe,
                "P/B (KBV)": pb,
                "Umsatz ($B)": market_cap_b,
                "Alpheon Score": score,
                "Dividendenrendite (%)": round(dividend_pct, 2)
            })
            
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Fehler bei {ticker}: {e}")
            continue

    df = pd.DataFrame(data_list)
    
    # Als CSV speichern
    df.to_csv("uni_snapshot.csv", index=False)
    print("Snapshot erfolgreich als uni_snapshot.csv gespeichert!")

if __name__ == "__main__":
    generate_snapshot()
