# billing.py
import streamlit as st
import stripe

stripe.api_key = "sk_test_DEIN_STRIPE_SECRET_KEY"

def render_stripe_checkout():
    """Rendert die Abrechnungsseite und verwaltet den Stripe Checkout in grauen Boxen."""
    
    # CSS für die grauen Boxen im Billing-Bereich
    st.markdown("""
        <style>
        .pricing-card {
            background-color: #ffffff;
            border: 1px solid #d0d7de;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        </style>
    """, unsafe_allow_html=True)

    # Korrekte Überschrift statt Markdown-Syntaxfehler
    st.markdown("## Abonnement & Billing")
    st.markdown("Schalte das volle **Alpheon Terminal Pro** frei, um uneingeschränkten Zugriff auf alle globalen Value-Screener und Live-Daten zu erhalten.")
    st.markdown("<br>", unsafe_allow_html=True)

    query_params = st.query_params
    if "session_id" in query_params:
        st.success("Vielen Dank! Dein Abonnement wurde erfolgreich aktiviert.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="pricing-card">
                <div>
                    <h3 style="margin-top: 0; color: #1f2328 !important;">Free Plan</h3>
                    <ul style="color: #57606a !important; padding-left: 20px; line-height: 1.6;">
                        <li>Standard-Screener</li>
                        <li>Begrenzte Filter</li>
                        <li>Wöchentliche Updates</li>
                    </ul>
                </div>
                <div>
                    <hr style="border: none; border-top: 1px solid #d0d7de; margin: 20px 0;">
                    <p style="font-weight: 600; color: #1f2328 !important; margin-bottom: 15px;">Kostenlos</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") 
        st.button("Aktueller Plan", disabled=True, key="free_plan_btn")

    with col2:
        st.markdown("""
            <div class="pricing-card">
                <div>
                    <h3 style="margin-top: 0; color: #1f2328 !important;">Pro Terminal</h3>
                    <ul style="color: #57606a !important; padding-left: 20px; line-height: 1.6;">
                        <li><b>Unbegrenzter Globaler Scan</b></li>
                        <li>Erweiterter Alpheon Score</li>
                        <li>Echtzeit-Bilanzen & Deep-Dives</li>
                        <li>CSV-Export aller Daten</li>
                    </ul>
                </div>
                <div>
                    <hr style="border: none; border-top: 1px solid #d0d7de; margin: 20px 0;">
                    <p style="font-weight: 600; color: #1f2328 !important; margin-bottom: 15px;">49 $ / Monat</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        if st.button("Jetzt Pro werden", key="stripe_checkout_btn"):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price': 'price_DEIN_STRIPE_PRICE_ID',
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='http://localhost:8501/?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url='http://localhost:8501/',
                    customer_email=st.session_state.get("user_email", ""),
                )
                
                st.markdown(f"""
                    <meta http-equiv="refresh" content="0;url={checkout_session.url}">
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Fehler beim Erstellen der Stripe-Session: {e}")