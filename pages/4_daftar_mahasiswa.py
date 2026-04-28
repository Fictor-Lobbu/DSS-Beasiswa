import streamlit as st
import pandas as pd
from database.db import connect_db
from utils.sidebar import sidebar

# 🔒 Proteksi Login
if "login" not in st.session_state or not st.session_state["login"]:
    st.switch_page("app.py")

sidebar()

st.title("Daftar Mahasiswa 👥")

conn = connect_db()
c = conn.cursor()

# Ambil daftar kriteria secara dinamis agar query INSERT nantinya akurat
cols_info = pd.read_sql_query("PRAGMA table_info(mahasiswa)", conn)
kriteria_list = cols_info[~cols_info['name'].isin(['id', 'nama', 'skor', 'ranking'])]['name'].tolist()

# Ambil semua data untuk ditampilkan
df = pd.read_sql_query("SELECT * FROM mahasiswa", conn)

if df.empty:
    st.info("Belum ada data mahasiswa yang terdaftar.")
else:
    st.subheader("Data Tersimpan")
    # Menampilkan tabel (ID akan terlihat selalu berurutan 1, 2, 3...)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # Bagian Hapus dengan Ikon Merah Aesthetic
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; color: #ef4444; margin-bottom: 10px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M10 11v6M14 11v6"/></svg>
            <h4 style="margin: 0;">Hapus Data</h4>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        col_select, col_btn = st.columns([2, 1])
        with col_select:
            id_to_del = st.selectbox(
                "Pilih ID Mahasiswa untuk dihapus", 
                df['id'].tolist(),
                format_func=lambda x: f"ID {x}: {df[df['id']==x]['nama'].values[0]}"
            )
        
        with col_btn:
            st.write("") # Spacer agar sejajar dengan selectbox
            if st.button("🗑️ Hapus Permanen", type="secondary", use_container_width=True):
                try:
                    # 1. Hapus data yang dipilih
                    c.execute("DELETE FROM mahasiswa WHERE id = ?", (id_to_del,))
                    
                    # 2. LOGIKA MENGATUR ULANG ID (RE-INDEXING)
                    # Ambil semua data sisa (kecuali ID lama)
                    kolom_str = ", ".join(["nama"] + kriteria_list)
                    c.execute(f"SELECT {kolom_str} FROM mahasiswa ORDER BY id")
                    rows = c.fetchall()
                    
                    # 3. Kosongkan tabel dan reset AI Counter
                    c.execute("DELETE FROM mahasiswa")
                    c.execute("DELETE FROM sqlite_sequence WHERE name='mahasiswa'")
                    
                    # 4. Masukkan kembali data agar ID teratur dari 1
                    if rows:
                        placeholders = ", ".join(["?"] * len(rows[0]))
                        c.executemany(f"INSERT INTO mahasiswa ({kolom_str}) VALUES ({placeholders})", rows)
                    
                    conn.commit()
                    st.success("Data dihapus dan ID telah diatur ulang secara otomatis.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

conn.close()