import streamlit as st
import pandas as pd

def data_transaksi():
    st.subheader("📂 Data Transaksi")
    uploaded_file = st.file_uploader("Upload File Excel/CSV (format transaksi)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")

            st.session_state['data_transaksi'] = df
            st.success("Data berhasil diupload!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file: {e}")

    elif 'data_transaksi' in st.session_state:
        st.dataframe(st.session_state['data_transaksi'])
    else:
        st.info("Silakan upload file transaksi terlebih dahulu.")
