import streamlit as st
import pandas as pd
from database.db import connect_db
from utils.helpers import validasi_ipk
from utils.sidebar import sidebar

# 🔒 Proteksi Login
if "login" not in st.session_state or not st.session_state["login"]:
    st.switch_page("app.py")

sidebar()

st.title("Input Data Mahasiswa 📝")
st.markdown("<p style='opacity: 0.8; margin-top: -10px;'>Tambahkan data kandidat beasiswa baru ke dalam sistem.</p>", unsafe_allow_html=True)

conn = connect_db()
c = conn.cursor()

# 🔍 1. Ambil kolom dari database secara otomatis
cols_info = pd.read_sql_query("PRAGMA table_info(mahasiswa)", conn)

# 2. Ambil semua kolom KECUALI kolom sistem
kriteria_list = cols_info[
    ~cols_info['name'].isin(['id', 'nama', 'skor', 'ranking'])
]['name'].tolist()

# UI CARD
st.markdown('<div class="card">', unsafe_allow_html=True)

nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama mahasiswa...")

col1, col2 = st.columns(2)
input_values = {}

# 🔄 Loop kriteria dinamis
for i, k in enumerate(kriteria_list):
    label = k.replace("_", " ").title()

    with col1 if i % 2 == 0 else col2:

        # 🔥 PERINGKAT (FIX UTAMA DI SINI)
        if k == 'peringkat':
            p_label = st.selectbox(
                "Peringkat Juara Umum",
                ["Juara 1", "Juara 2", "Juara 3"],
                key="key_peringkat"
            )

            # ✅ Nilai asli (natural)
            raw_map = {
                "Juara 1": 1,
                "Juara 2": 2,
                "Juara 3": 3
            }

            nilai_asli = raw_map[p_label]

            # 🔥 Transformasi ke benefit (MOORA)
            nilai_transform = 4 - nilai_asli

            input_values[k] = nilai_transform

        # 📄 SURAT
        elif k == 'surat':
            s_label = st.selectbox(
                "Surat Keterangan",
                ["Tersedia", "Tidak Tersedia"],
                key="key_surat"
            )
            input_values[k] = 1 if s_label == "Tersedia" else 0

        # 🎓 IPK
        elif k == 'ipk':
            ipk_val = st.number_input(
                "IPK (Minimal 3.25)",
                min_value=0.0, max_value=4.0, step=0.01, value=3.25,
                key="key_ipk"
            )

            input_values[k] = ipk_val

            # 🔥 KETERANGAN SKALA IPK
            if 3.25 <= ipk_val <= 3.70:
                skala = 1
            elif 3.71 <= ipk_val <= 3.90:
                skala = 2
            elif 3.91 <= ipk_val <= 4.00:
                skala = 3
            else:
                skala = None

            # Tampilkan ke user
            if skala:
                st.info(f"📊 Skala IPK: {skala}")

        # 🔄 KRITERIA TAMBAHAN (DINAMIS)
        else:
            input_values[k] = st.number_input(
                f"Nilai {label}",
                min_value=0.0,
                value=0.0,
                step=0.1,
                key=f"key_{k}"
            )

st.markdown('</div>', unsafe_allow_html=True)

# 🚀 SIMPAN DATA
if st.button("Simpan Data", type="primary", use_container_width=True):

    if not nama:
        st.warning("Nama wajib diisi!")

    elif 'ipk' in input_values and not validasi_ipk(input_values['ipk']):
        st.error("Gagal: IPK minimal harus 3.25.")

    else:
        try:
            cols = ", ".join(["nama"] + list(input_values.keys()))
            placeholders = ", ".join(["?"] * (len(input_values) + 1))
            vals = [nama] + list(input_values.values())

            c.execute(f"INSERT INTO mahasiswa ({cols}) VALUES ({placeholders})", vals)
            conn.commit()

            st.success(f"✅ Data {nama} berhasil disimpan!")
            st.rerun()

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menyimpan: {e}")

conn.close()