import streamlit as st
import base64
import os

# 1. Gunakan cache agar logo tidak dikonversi ulang setiap kali loading (mempercepat rendering)
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def sidebar():
    # 2. Letakkan CSS sedini mungkin. 
    # Gunakan selektor yang lebih agresif untuk menyembunyikan navigasi asli
    st.markdown("""
        <style>
            /* Sembunyikan navigasi bawaan secepat mungkin */
            section[data-testid="stSidebar"] > div { padding-top: 0px; }
            [data-testid="stSidebarNav"] { display: none !important; }
            
            /* Stabilkan lebar sidebar agar tidak goyang saat loading */
            [data-testid="stSidebar"] { min-width: 250px; }

            .card {
                background-color: var(--secondary-background-color);
                padding: 24px;
                border-radius: 12px;
                border: 1px solid rgba(128, 128, 128, 0.2);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                margin-bottom: 20px;
                transition: all 0.3s ease;
            }
            /* ... Sisa CSS Anda tetap sama ... */
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # 3. Logo
        logo_path = "assets/unklab_logo.png"
        if os.path.exists(logo_path):
            img_base64 = get_base64_of_bin_file(logo_path)
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; margin-top: 5px; margin-bottom: 5px;">
                    <img src="data:image/png;base64,{img_base64}" style="width: 42px; height: auto;">
                    <span style="font-size: 16px; font-weight: 600; line-height: 1.2; color: var(--text-color);">
                        Universitas<br>Klabat
                    </span>
                </div>
                <hr style="margin-top: 15px; margin-bottom: 20px; border: none; border-top: 1px solid rgba(128, 128, 128, 0.2);">
                """, unsafe_allow_html=True
            )

        # 4. Gunakan Menu Navigasi
        # Tips: Pastikan urutan page_link ini selalu konsisten di semua halaman
        st.page_link("app.py", label="Home", icon=":material/home:")
        st.page_link("pages/0_bobot_kriteria.py", label="Bobot Kriteria", icon=":material/balance:")
        st.page_link("pages/1_input_data.py", label="Input Data", icon=":material/edit_document:")
        st.page_link("pages/4_daftar_mahasiswa.py", label="Daftar Mahasiswa", icon=":material/group:")
        st.page_link("pages/2_proses_dss.py", label="Proses DSS", icon=":material/analytics:")
        st.page_link("pages/3_hasil.py", label="Hasil", icon=":material/leaderboard:")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Gunakan key unik agar tombol tidak konflik saat rerun
        if st.button("Logout", icon=":material/logout:", use_container_width=True, key="logout_btn"):
            st.session_state.clear()
            st.switch_page("app.py")