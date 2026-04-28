import streamlit as st
import pandas as pd
from database.db import connect_db
from utils.sidebar import sidebar
from utils.export_excel import export_to_excel

# 🔒 Proteksi Login
if "login" not in st.session_state or not st.session_state["login"]:
    st.switch_page("app.py")

sidebar()
st.title("Hasil Perankingan 🏆")

# =====================
# RESET FUNCTION
# =====================
def reset_ranking():
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE mahasiswa SET skor = NULL, ranking = NULL")
    conn.commit()
    conn.close()

    if "bobot_bwm" in st.session_state:
        del st.session_state["bobot_bwm"]

    if "kriteria_bwm" in st.session_state:
        del st.session_state["kriteria_bwm"]

    if "bo_vector" in st.session_state:
        del st.session_state["bo_vector"]

    if "ow_vector" in st.session_state:
        del st.session_state["ow_vector"]

    st.rerun()

# =====================
# AMBIL DATA
# =====================
conn = connect_db()
df = pd.read_sql_query(
    "SELECT * FROM mahasiswa WHERE ranking IS NOT NULL ORDER BY ranking ASC",
    conn
)
conn.close()

# =====================
# TAMPILKAN HASIL
# =====================
if df.empty:
    st.info("Belum ada hasil perankingan.")
else:
    top_name = df.iloc[0]['nama']

    st.markdown(f"""
    <div class="card" style="border-left: 5px solid #3b82f6;">
        <div class="card-title">Rekomendasi Utama</div>
        <div class="card-content"><b>{top_name}</b> menempati peringkat tertinggi.</div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df[['nama', 'skor', 'ranking']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "skor": st.column_config.NumberColumn("Skor", format="%.4f")
        }
    )

    # =====================
    # EXPORT EXCEL
    # =====================
    st.markdown("---")
    st.subheader("📥 Export Hasil ke Excel")

    if "bobot_bwm" in st.session_state and "kriteria_bwm" in st.session_state:

        if st.button("📊 Generate Excel"):

            filename = "hasil_dss.xlsx"

            export_to_excel(
                df,
                st.session_state["bobot_bwm"],
                st.session_state["kriteria_bwm"],
                bo=st.session_state.get("bo_vector"),
                ow=st.session_state.get("ow_vector"),
                filename=filename
            )

            st.success("✅ File Excel berhasil dibuat!")

            with open(filename, "rb") as f:
                st.download_button(
                    label="⬇️ Download Excel",
                    data=f,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    else:
        st.warning("⚠️ Hitung bobot BWM terlebih dahulu!")

    # =====================
    # RESET ONLY
    # =====================
    st.markdown("---")

    with st.popover("⚠️ Reset"):
        if st.button("Hapus Semua Data Hasil"):
            reset_ranking()