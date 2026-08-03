# app.py
import streamlit as st
import pandas as pd
from config import get_massive_global_universe
from backend import fetch_screened_data, fetch_historical_data
from auth import render_auth_sidebar, init_auth_state
from billing import render_stripe_checkout

st.set_page_config(
    page_title="Alpheon Terminal", 
    page_icon="■", 
    layout="wide"
)

# STYLING (Light-Theme, 75x75 Logo-Box mit komplett schwarzem Icon)
st.markdown("""
    <style>
    /* 1. Globaler Light Mode */
    .stApp, header[data-testid="stHeader"] {
        background-color: #f4f6f8 !important;
        color: #1f2328 !important;
    }
    
    /* Sidebar komplett hellgrau */
    [data-testid="stSidebar"] {
        background-color: #ebf0f4 !important;
        border-right: 1px solid #d0d7de;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #1f2328 !important;
    }

    /* 2. Login-Button & Logout-Button in Rolex-Grün */
    div.stButton > button {
        background-color: #006039 !important;
        color: #ffffff !important;
        border: none !important;
        width: 100%;
        font-weight: 600;
        border-radius: 6px;
    }
    div.stButton > button:hover {
        background-color: #004d2e !important;
    }

    /* 3. Input-Felder */
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
    }
    
    div.stTextInput input, div.stPasswordInput input {
        background-color: transparent !important;
        color: #1f2328 !important;
        -webkit-text-fill-color: #1f2328 !important;
    }

    /* 4. Passwort-Sichtbarkeits-Button (Auge) */
    div[data-baseweb="input"] button {
        background-color: #f6f8fa !important;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        border-left: 1px solid #d0d7de !important;
    }
    div[data-baseweb="input"] button svg {
        fill: #57606a !important;
    }
    div[data-baseweb="input"] button:hover {
        background-color: #eaeef2 !important;
    }

    /* 5. Logo & Header ganz oben in der Sidebar (75px x 75px) */
    .alpheon-brand-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 10px;
        padding-bottom: 15px;
        border-bottom: 1px solid #d0d7de;
    }
    .alpheon-logo-box {
        width: 75px !important;
        height: 75px !important;
        background-color: #0b0e14 !important; /* Schwarzer Hintergrund */
        border: 1px solid #1f2328 !important;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .alpheon-logo-box svg {
        width: 44px !important;
        height: 44px !important;
    }
    .alpheon-brand-text {
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-transform: uppercase;
        color: #1f2328 !important;
        margin: 0;
        line-height: 1.1;
    }
    .alpheon-brand-text span {
        color: #006039 !important; /* Rolex-Grün */
        display: block;
        font-size: 13px;
    }
    
    .hero-box {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        padding: 40px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        padding: 24px;
        border-radius: 8px;
        height: 180px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* 6. Weiße Box für die oberen Kennzahlen/Metriken */
    .metrics-container {
        background-color: #ffffff;
        border: 1px solid #d0d7de;
        padding: 20px 25px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)

# INITIALISIERUNG
init_auth_state()

# Prüfen, ob der Nutzer im Free-Modus ist (Annahme: "is_premium" steuert den Status)
is_free_user = not st.session_state.get("is_premium", False)

# --- SEITENLEISTE (Logo 75x75px, innerer Balken schwarz) ---
with st.sidebar:
    st.markdown("""
        <div class="alpheon-brand-container">
            <div class="alpheon-logo-box">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 10L30 28H25L20 18L15 28H10L20 10Z" fill="#006039"/>
                    <path d="M12 24H28" stroke="#0b0e14" stroke-width="2"/>
                </svg>
            </div>
            <h2 class="alpheon-brand-text">ALPHEON <span>TERMINAL</span></h2>
        </div>
    """, unsafe_allow_html=True)
    
    render_auth_sidebar()

# --- HAUPTBEREICH ---
if not st.session_state["authenticated"]:
    st.markdown("""
        <div class="hero-box" style="margin-top: 20px;">
            <h1 style="color: #1f2328 !important; margin-bottom: 10px; font-size: 32px;">Institutionelles Value-Screening für globale Märkte</h1>
            <p style="color: #57606a !important; font-size: 18px; margin: 0;">Alpheon Terminal eliminiert Rauschen und identifiziert systematisch unterbewertete Aktien nach strengen fundamentalen Parametern (Graham & Buffett Methodik).</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: #1f2328 !important; margin-top: 0; font-size: 18px;">1. Globaler Scan</h3>
                <p style="color: #57606a !important; font-size: 14px; line-height: 1.5;">Über 1,000 handverlesene Standardwerte aus Nordamerika, Europa und dem Asien-Pazifik-Raum in Echtzeit gefiltert.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: #1f2328 !important; margin-top: 0; font-size: 18px;">2. Alpheon Score</h3>
                <p style="color: #57606a !important; font-size: 14px; line-height: 1.5;">Ein proprietäres Bewertungssystem (0–100 Punkte), das Bilanzen, KGV, KBV und Dividenden bündelt.</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style="color: #1f2328 !important; margin-top: 0; font-size: 18px;">3. Keine Value-Fallen</h3>
                <p style="color: #57606a !important; font-size: 14px; line-height: 1.5;">Schütze dein Kapital vor scheinbar günstigen Aktien durch harte Kennzahlen-Prüfung und saubere Daten.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Bitte verwenden Sie die Seitenleiste links, um sich anzumelden oder ein neues Konto zu erstellen.")

else:
    nav_tab = st.sidebar.selectbox("Navigation", ["Market Screener", "Abonnement (Billing)"], key="main_nav_selector")
    
    if nav_tab == "Abonnement (Billing)":
        render_stripe_checkout()
    else:
        st.sidebar.markdown("---")
        st.sidebar.header("Filterparameter")
        min_score = st.sidebar.slider("Min. Alpheon Score", min_value=0, max_value=100, value=50, step=5)
        max_pe = st.sidebar.slider("Max. P/E Ratio (KGV)", min_value=0.01, max_value=100.0, value=15.0, step=1.0)
        max_pb = st.sidebar.slider("Max. P/B Ratio (KBV)", min_value=0.5, max_value=20.0, value=1.5, step=0.1)
        min_revenue_b = st.sidebar.slider("Min. Umsatz (Mrd. USD)", min_value=0.5, max_value=10000.0, value=2.0, step=0.5)

        @st.cache_data(ttl=3600)
        def load_data():
            return fetch_screened_data()

        with st.spinner("Analysiere globale Bilanzen und Marktdaten..."):
            df = load_data()

        if not df.empty:
            filtered_df = df[
                (df["Alpheon Score"] >= min_score) &
                (df["Umsatz ($B)"] >= min_revenue_b) & 
                (df["P/E (KGV)"] > 0) & 
                (df["P/E (KGV)"] <= max_pe) & 
                (df["P/B (KBV)"] > 0) & 
                (df["P/B (KBV)"] <= max_pb)
            ]
            
            filtered_df = filtered_df.sort_values(by="Alpheon Score", ascending=False)

            # --- GRATIS-PLAN EINSCHRÄNKUNG: Max. 50 Aktien ---
            if is_free_user and not filtered_df.empty:
                filtered_df = filtered_df.head(50)

            # Metriken in einer sauberen weißen Box im Hauptbereich
            st.markdown('<div class="metrics-container" style="margin-top: 10px;">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Treffer", len(filtered_df))
            c2.metric("Ø Alpheon Score", f"{filtered_df['Alpheon Score'].mean():.1f}" if not filtered_df.empty else "0")
            c3.metric("Ø KGV", f"{filtered_df['P/E (KGV)'].mean():.1f}" if not filtered_df.empty else "0")
            c4.metric("Ø Dividendenrendite", f"{filtered_df['Dividendenrendite (%)'].mean():.2f}%" if not filtered_df.empty else "0")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")

            tab_table, tab_deepdive, tab_export = st.tabs(["Screener Ergebnisse", "Einzeltitel-Analyse", "Export"])

            with tab_table:
                st.dataframe(filtered_df, use_container_width=True)
                if is_free_user:
                    st.info("💡 **Free-Modus:** Du siehst hier die ersten 50 Aktien. Hole dir Premium, um alle Ergebnisse uneingeschränkt einzusehen.")

            with tab_deepdive:
                if is_free_user:
                    st.warning("🔒 **Premium-Feature:** Die Einzeltitel-Analyse mit interaktiven Kursgraphen ist exklusiv für Premium-Mitglieder verfügbar. Wechsle zum Tab 'Abonnement (Billing)', um freizuschalten.")
                else:
                    if not filtered_df.empty:
                        selected_ticker = st.selectbox("Ticker auswählen:", filtered_df["Ticker"].unique())
                        selected_row = filtered_df[filtered_df["Ticker"] == selected_ticker].iloc[0]
                        
                        d1, d2, d3 = st.columns(3)
                        d1.text(f"Unternehmen: {selected_row['Unternehmen']}")
                        d2.text(f"Sektor: {selected_row['Sektor']}")
                        d3.text(f"Alpheon Score: {selected_row['Alpheon Score']} / 100")
                        
                        hist_close = fetch_historical_data(selected_ticker)
                        if hist_close is not None and not hist_close.empty:
                            st.line_chart(hist_close)
                        else:
                            st.warning("Keine Kursdaten verfügbar.")

            with tab_export:
                if is_free_user:
                    st.warning("🔒 **Premium-Feature:** Der CSV-Export von Reports ist im Gratis-Modus deaktiviert.")
                else:
                    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="CSV Report herunterladen",
                        data=csv_data,
                        file_name="alpheon_value_report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        else:
            st.warning("Keine Aktien entsprechen den Kriterien.")
