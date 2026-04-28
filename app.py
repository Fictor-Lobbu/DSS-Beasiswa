import streamlit as st
from login import login
from utils.sidebar import sidebar

st.set_page_config(page_title="DSS Beasiswa", layout="wide", initial_sidebar_state="expanded")

# session login
if "login" not in st.session_state:
    st.session_state["login"] = False

# 🔒 JIKA BELUM LOGIN
if not st.session_state["login"]:
    # Sembunyikan sidebar bawaan saat di halaman login
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

    login()

# ✅ JIKA SUDAH LOGIN
else:
    # 🔹 Panggil Sidebar (Ini sekaligus akan menyuntikkan Global CSS untuk Card ke semua halaman)
    sidebar()

    # 🔹 HEADER
    st.title("Sistem DSS Beasiswa")
    st.markdown(f"<div class='welcome-text'>Selamat datang, <b>{st.session_state.get('username', 'Admin')}</b> 👋</div>", unsafe_allow_html=True)

    # 🔹 GRID LAYOUT
    col1, col2 = st.columns(2)

    # 📌 DESKRIPSI (Icon: Book Open)
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                </svg>
                Deskripsi Sistem
            </div>
            <div class="card-content">
                Sistem ini membantu pengambilan keputusan penerima beasiswa secara objektif dengan metode:
                <br><br>
                • <b>BWM</b> untuk menentukan bobot kriteria<br>
                • <b>MOORA</b> untuk proses perankingan
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 🎯 KRITERIA (Icon: Target/Crosshair)
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="6"></circle>
                    <circle cx="12" cy="12" r="2"></circle>
                </svg>
                Kriteria Penilaian
            </div>
            <div class="card-content">
                <b>C1:</b> Prestasi Umum<br>
                <b>C2:</b> Surat Keterangan Kepala Sekolah<br>
                <b>C3:</b> IPK Minimal (≥ 3.25)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 🔽 FULL WIDTH
    # 📊 ALUR SISTEM (Icon: Git Merge / Alur)
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="18" cy="18" r="3"></circle>
                <circle cx="6" cy="6" r="3"></circle>
                <path d="M13 6h3a2 2 0 0 1 2 2v7"></path>
                <line x1="6" y1="9" x2="6" y2="21"></line>
            </svg>
            Alur Sistem
        </div>
        <div class="card-content">
            <div style="display: flex; gap: 15px; align-items: center; flex-wrap: wrap;">
                <span><b>1.</b> Hitung Bobot Kriteria (BWM)</span> 
                <span style="color: #3b82f6; font-weight: bold;">→</span> 
                <span><b>2.</b> Input Data Mahasiswa</span> 
                <span style="color: #3b82f6; font-weight: bold;">→</span> 
                <span><b>3.</b> Proses Perankingan (MOORA)</span> 
                <span style="color: #3b82f6; font-weight: bold;">→</span> 
                <span><b>4.</b> Tampilkan Hasil</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ STATUS (Icon: Shield Check)
    st.markdown("""
    <div class="card" style="border-left: 4px solid #10b981;">
        <div class="card-title">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <polyline points="9 12 11 14 15 10"></polyline>
            </svg>
            Status Sistem
        </div>
        <div class="card-content">
            Sistem saat ini <b>Online</b> dan siap digunakan untuk melakukan perhitungan penentuan penerima beasiswa.
        </div>
    </div>
    """, unsafe_allow_html=True)