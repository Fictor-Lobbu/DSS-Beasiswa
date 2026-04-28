import streamlit as st
import pandas as pd
from database.db import connect_db
from modules.dss import proses_dss
from utils.sidebar import sidebar

# 🔒 Proteksi Login
if "login" not in st.session_state or not st.session_state["login"]:
    st.switch_page("app.py")

sidebar()
st.title("Proses Perankingan (MOORA) ⚙️")

conn = connect_db()
df = pd.read_sql_query("SELECT * FROM mahasiswa", conn)

if df.empty:
    st.warning("Data mahasiswa kosong. Silakan input data terlebih dahulu.")
else:
    st.subheader("Data yang akan diproses")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    if st.button("🚀 Jalankan Ranking", type="primary", use_container_width=True):

        # ✅ Validasi bobot
        if "bobot_bwm" not in st.session_state:
            st.error("⚠️ Hitung bobot BWM terlebih dahulu!")
            st.stop()

        # ✅ Validasi kriteria
        if "kriteria_bwm" not in st.session_state:
            st.error("⚠️ Urutan kriteria tidak ditemukan!")
            st.stop()

        bobot = st.session_state["bobot_bwm"]
        kriteria_bwm = st.session_state["kriteria_bwm"]

        try:
            # 🔥 Ambil data sesuai urutan BWM
            data_kriteria = df[kriteria_bwm].values

            # 🔥 Hitung MOORA
            skor = proses_dss(data_kriteria, bobot)

            # 🔥 Ranking
            df['skor'] = skor
            df_ranked = df.sort_values(by='skor', ascending=False).copy()
            df_ranked['ranking'] = range(1, len(df_ranked) + 1)

            # 🔥 Simpan ke database
            c = conn.cursor()
            for _, row in df_ranked.iterrows():
                c.execute("""
                    UPDATE mahasiswa 
                    SET skor = ?, ranking = ? 
                    WHERE id = ?
                """, (float(row['skor']), int(row['ranking']), int(row['id'])))

            conn.commit()

            # ✅ NOTIFIKASI SAJA
            st.success("✅ Perankingan berhasil! Silakan lihat hasil di menu 'Hasil'.")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

conn.close()