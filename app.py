import streamlit as st
from streamlit_option_menu import option_menu

from login import login_page
from transaksi import data_transaksi
from proses import proses_apriori
from hasil import hasil
from visualisasi import visualisasi
from register import register_admin
from utils import load_css, header_footer

def main_menu():
    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Halaman Utama", "Data Transaksi", "Proses Apriori", "Hasil","Visualisasi", "Register Admin", "Logout"],
            icons=["house", "database", "cpu", "bar-chart", "person-plus", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Halaman Utama":
        st.subheader("🏠 Halaman Utama")
        st.markdown("""
        <h3 style='text-align:center;'>Selamat Datang</h3>
        <p style='text-align:center;'>Implementasi Data Mining untuk menemukan Produk Batik yang paling banyak diminati dengan Algoritma Apriori.</p>
        """, unsafe_allow_html=True)

    elif selected == "Data Transaksi":
        data_transaksi()
    elif selected == "Proses Apriori":
        proses_apriori()
    elif selected == "Hasil":
        hasil()
    elif selected == "Visualisasi":
        visualisasi()
    elif selected == "Register Admin":
        register_admin()
    elif selected == "Logout":
        st.session_state["login"] = False
        st.success("✅ Anda berhasil logout.")
        st.rerun()

def main():
    load_css()
    header_footer()
    if "login" not in st.session_state:
        st.session_state["login"] = False

    if st.session_state["login"]:
        main_menu()
    else:
        login_page()

if __name__ == "__main__":
    st.set_page_config(page_title="Apriori Batik", layout="wide")
    main()
