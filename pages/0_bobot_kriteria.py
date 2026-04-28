import streamlit as st
import pandas as pd
import numpy as np
from database.db import connect_db
from modules.bwm import calculate_bwm_weights
from utils.sidebar import sidebar

# 🔒 Proteksi Login
if "login" not in st.session_state or not st.session_state["login"]:
    st.switch_page("app.py")

sidebar()

st.title("Manajemen Kriteria & Bobot ⚖️")

conn = connect_db()
c = conn.cursor()

# 🔹 1. TAB MENU UNTUK PEMISAHAN FITUR (CLEAN UI)
tab1, tab2 = st.tabs(["⚙️ Pengaturan Kriteria", "📊 Hitung Bobot BWM"])

# --- TAB 1: MANAJEMEN KRITERIA (CRUD) ---
with tab1:
    st.subheader("Manajemen Kriteria")
    st.info("Gunakan bagian ini untuk menambah atau menghapus kriteria penilaian beasiswa.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2, gap="large")
    
    # --- BAGIAN TAMBAH ---
    with col_a:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 600;">Tambah Kriteria</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            new_kriteria = st.text_input("Nama Kriteria Baru", placeholder="Contoh: Keaktifan Organisasi", key="input_tambah")
            
            if st.button("➕ Tambah Kriteria", type="primary", use_container_width=True):
                if new_kriteria:
                    # Normalisasi nama kolom
                    col_name = new_kriteria.lower().strip().replace(" ", "_")
                    
                    # Cek eksistensi kolom
                    existing_cols = pd.read_sql_query("PRAGMA table_info(mahasiswa)", conn)['name'].tolist()
                    
                    if col_name in existing_cols:
                        st.warning(f"⚠️ Kriteria '{new_kriteria}' sudah ada.")
                    else:
                        try:
                            c.execute(f"ALTER TABLE mahasiswa ADD COLUMN {col_name} REAL DEFAULT 0")
                            conn.commit()
                            st.success(f"✅ Kriteria '{new_kriteria}' berhasil ditambahkan!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menambah kriteria: {e}")
                else:
                    st.warning("Nama kriteria tidak boleh kosong.")

    # --- BAGIAN HAPUS ---
    with col_b:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M10 11v6M14 11v6"/></svg>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 600; color: #ef4444;">Hapus Kriteria</h3>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            cols_info = pd.read_sql_query("PRAGMA table_info(mahasiswa)", conn)
            list_kriteria = cols_info[~cols_info['name'].isin(['id', 'nama', 'skor', 'ranking'])]['name'].tolist()
            
            if list_kriteria:
                target_del = st.selectbox("Pilih kriteria untuk dihapus", list_kriteria, key="select_hapus")
                
                if st.button("🗑️ Hapus Permanen", type="secondary", use_container_width=True):
                    try:
                        c.execute(f"ALTER TABLE mahasiswa DROP COLUMN {target_del}")
                        conn.commit()
                        st.success(f"✅ Kriteria '{target_del}' berhasil dihapus!")
                        st.rerun()
                    except Exception as e:
                        st.error("Gagal menghapus. Versi SQLite Anda mungkin memerlukan migrasi manual.")
            else:
                st.write("Tidak ada kriteria untuk dihapus.")

# --- TAB 2: PERHITUNGAN BWM ---
with tab2:
    st.subheader("Hitung Bobot BWM")
    
    # 1. Ambil kriteria terbaru dari database
    cols_now = pd.read_sql_query("PRAGMA table_info(mahasiswa)", conn)
    
    # 2. Ambil SEMUA kriteria secara dinamis (tanpa dibatasi list manual)
    current_kriteria = cols_now[~cols_now['name'].isin(['id', 'nama', 'skor', 'ranking'])]['name'].tolist()

    if not current_kriteria:
        st.warning("Silakan tambah kriteria terlebih dahulu di tab 'Pengaturan Kriteria'.")
    else:
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <small>💡 <b>Tips:</b> Beri nilai 1 pada kriteria <b>Best</b> (di kiri) dan nilai 1 pada kriteria <b>Worst</b> (di kanan).</small>
        </div>
        """, unsafe_allow_html=True)

        col_bo, col_ow = st.columns(2, gap="large")
        bo_vector = []
        ow_vector = []

        with col_bo:
            st.markdown("#### 🥇 Best to Others")
            for k in current_kriteria:
                label = k.replace("_", " ").title()
                # Input nilai perbandingan Best vs Kriteria J
                val = st.number_input(f"Best vs {label}", 1, 9, 1, key=f"bo_{k}")
                bo_vector.append(val)

        with col_ow:
            st.markdown("#### 👎 Others to Worst")
            for k in current_kriteria:
                label = k.replace("_", " ").title()
                # Input nilai perbandingan Kriteria J vs Worst
                val = st.number_input(f"{label} vs Worst", 1, 9, 1, key=f"ow_{k}")
                ow_vector.append(val)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Simpan & Kalkulasi Bobot", type="primary", use_container_width=True):
            # Validasi aturan BWM (Harus ada angka 1 di kedua vektor)
            if 1 not in bo_vector:
                st.error("⚠️ Di kolom Best, harus ada satu kriteria yang bernilai 1 sebagai acuan kriteria terbaik.")
            elif 1 not in ow_vector:
                st.error("⚠️ Di kolom Worst, harus ada satu kriteria yang bernilai 1 sebagai acuan kriteria terburuk.")
            else:
                try:
                    # Hitung bobot menggunakan modul BWM
                    weights, ksi = calculate_bwm_weights(bo_vector, ow_vector)
                    st.session_state["bobot_bwm"] = weights
                    
                    st.session_state["kriteria_bwm"] = current_kriteria

                    st.session_state["bo_vector"] = bo_vector
                    st.session_state["ow_vector"] = ow_vector

                    st.success(f"✅ Berhasil! Nilai Konsistensi (Ksi): {ksi:.4f}")
                    
                    # Tampilkan hasil dalam bentuk tabel yang rapi
                    df_res = pd.DataFrame({
                        "Kriteria": [k.replace("_", " ").title() for k in current_kriteria],
                        "Bobot Desimal": np.round(weights, 4),
                        "Bobot (%)": [f"{w*100:.2f}%" for w in weights]
                    })
                    st.dataframe(df_res, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Gagal menghitung bobot: {e}")

conn.close()