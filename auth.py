# auth.py
import streamlit as st
import sqlite3
import bcrypt

def get_db_connection():
    """Stellt eine Verbindung zur SQLite-Datenbank her und erstellt die Tabelle falls nötig."""
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

def init_auth_state():
    """Initialisiert den Authentifizierungs-Status in der Session."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = ""

def render_auth_sidebar():
    """Rendert die Login- und Registrierungsmaske in der Sidebar mit echter SQLite-Datenbank."""
    st.markdown("### Benutzerkonto")
    
    if st.session_state["authenticated"]:
        st.success(f"Eingeloggt als:\n**{st.session_state['user_email']}**")
        st.info("Status: Pro-Modus / Aktiv" if "admin" in st.session_state['user_email'] else "Status: Free-Modus")
        
        if st.button("Abmelden", key="logout_btn"):
            st.session_state["authenticated"] = False
            st.session_state["user_email"] = ""
            st.rerun()
    else:
        # Eindeutiger Key für den Radio-Button
        auth_mode = st.sidebar.radio("Modus", ["Anmelden", "Registrieren"], key="auth_mode_selector", label_visibility="collapsed")
        
        email = st.text_input("E-Mail-Adresse", key="auth_email_input").strip().lower()
        password = st.text_input("Passwort", type="password", key="auth_password_input")
        
        conn, cursor = get_db_connection()
        
        if auth_mode == "Anmelden":
            if st.button("Login", key="login_action_btn"):
                if not email or not password:
                    st.warning("Bitte E-Mail und Passwort eingeben.")
                else:
                    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
                    row = cursor.fetchone()
                    
                    if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = email
                        st.success("Erfolgreich angemeldet!")
                        st.rerun()
                    else:
                        st.error("Ungültige E-Mail oder falsches Passwort.")
        else:
            if st.button("Konto erstellen", key="register_action_btn"):
                if not email or not password:
                    st.warning("Bitte E-Mail und Passwort eingeben.")
                else:
                    # Prüfen, ob E-Mail bereits existiert
                    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
                    if cursor.fetchone():
                        st.error("Diese E-Mail ist bereits registriert.")
                    else:
                        # Passwort sicher hashen
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        
                        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
                        conn.commit()
                        
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = email
                        st.success("Konto erstellt und eingeloggt!")
                        st.rerun()
        
        conn.close()