import streamlit as st
import base64
import os
from database.db import connect_db

# Fungsi untuk mengubah gambar lokal menjadi Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def login():

    st.markdown("""
        <style>
            /* 1. KUNCI HALAMAN AGAR TIDAK BISA DI-SCROLL PADA SEMUA CONTAINER STREAMLIT */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
                overflow: hidden !important;
                height: 100vh !important;
                max-height: 100vh !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Menyembunyikan scrollbar secara paksa untuk semua browser */
            ::-webkit-scrollbar {
                display: none !important;
            }
            * {
                -ms-overflow-style: none !important;
                scrollbar-width: none !important;
            }

            .stApp {
                background-color: #0f172a !important; 
            }

            [data-testid="stSidebar"], [data-testid="stHeader"] {
                display: none !important;
            }

            /* 2. MENENGAHKAN FORM SECARA VERTIKAL TANPA PADDING (Mencegah Overflow) */
            .block-container {
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                height: 100vh !important;
                padding-top: 0px !important; 
                padding-bottom: 0px !important;
            }

            /* 3. STYLING CARD (Targeting Kolom Tengah) */
            [data-testid="stHorizontalBlock"] > div:nth-child(2) {
                background-color: #1e293b !important; 
                padding: 3rem 2.5rem !important;      
                border-radius: 15px !important;       
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important; 
                border: 1px solid #334155 !important; 
            }

            /* 4. MENGHILANGKAN ICON MATA GANDA BAWAAN BROWSER (EDGE/CHROME) */
            input[type="password"]::-ms-reveal,
            input[type="password"]::-ms-clear,
            input[type="password"]::-webkit-reveal {
                display: none !important;
            }

            /* 5. PERBAIKAN WARNA INPUT FIELD */
            div[data-baseweb="input"] {
                background-color: #0f172a !important; 
                border-radius: 8px !important;
                border: 1px solid #475569 !important;
            }
            
            div[data-baseweb="input"] > div {
                background-color: transparent !important;
            }

            input {
                color: white !important;
                -webkit-text-fill-color: white !important; 
            }

            label {
                color: #cbd5e1 !important;
                font-size: 14px !important;
                margin-bottom: 5px !important;
            }

            div[data-testid="InputInstructions"] {
                display: none !important;
            }

            /* 6. MEMAKSA TOMBOL LOGIN FULL WIDTH */
            [data-testid="baseButton-secondary"] {
                width: 100% !important;
                height: 45px !important;
                border-radius: 8px !important;
                background-color: #3b82f6 !important; 
                color: white !important;
                font-weight: bold !important;
                border: none !important;
                margin-top: 20px !important;
                transition: all 0.3s ease !important;
            }
            
            [data-testid="baseButton-secondary"]:hover {
                background-color: #2563eb !important; 
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        # 🔹 LOGO
        logo_path = "assets/unklab_logo.png"
        
        if os.path.exists(logo_path):
            img_base64 = get_base64_of_bin_file(logo_path)
            st.markdown(
                f"""
                <div style="display: flex; justify-content: center; width: 100%; margin-bottom: 10px;">
                    <img src="data:image/png;base64,{img_base64}" width="120">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("Logo tidak ditemukan di folder assets.")

        # 🔹 JUDUL
        st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 25px;'>Login</h2>", unsafe_allow_html=True)

        # 🔹 INPUT
        username = st.text_input("Username", placeholder="Masukkan username")
        password = st.text_input("Password", type="password", placeholder="Masukkan password")

        # 🔹 BUTTON
        if st.button("Login"):
            conn = connect_db()
            c = conn.cursor()

            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            user = c.fetchone()
            conn.close()

            if user:
                st.session_state["login"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Username atau password salah!")