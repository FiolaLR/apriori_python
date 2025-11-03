import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def proses_apriori():
    st.subheader("⚙️ Proses Apriori")

    if 'data_transaksi' not in st.session_state:
        st.warning("⚠️ Belum ada data transaksi yang diupload.")
        return

    df = st.session_state['data_transaksi']
    st.write("Data yang digunakan:")
    st.dataframe(df)

    # Perbaikan data
    df['no bon'] = df['no bon'].ffill()
    df = df.dropna(subset=['no bon', 'kd_brg'])
    df = df.drop_duplicates()

    min_support = st.slider("Minimal Support", 0.0, 1.0, 0.05, 0.01)
    min_confidence = st.slider("Minimal Confidence", 0.0, 1.0, 0.3, 0.01)

    if st.button("⚙️ Jalankan Apriori", use_container_width=True):
        try:
            # Buat basket
            basket = (
                df.groupby(['no bon', 'kd_brg'])['kd_brg']
                .count()
                .unstack()
                .fillna(0)
                .applymap(lambda x: 1 if x >= 1 else 0)
            )
            basket = basket[basket.sum(axis=1) > 1]

            st.write("Basket hasil pivot:")
            st.dataframe(basket.head())

            # Jalankan Apriori
            frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)

            if frequent_itemsets.empty:
                st.warning("⚠️ Tidak ada itemset yang memenuhi nilai support.")
                return

            # Tambah kolom panjang itemset (untuk filter k=1, k=2, k=3)
            frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

            st.write("### ✅ Frequent Itemsets (Semua)")
            st.dataframe(frequent_itemsets)

            st.write("### ✅ Frequent Itemset k = 2")
            st.dataframe(frequent_itemsets[frequent_itemsets['length'] == 2])

            st.write("### ✅ Frequent Itemset k = 3")
            st.dataframe(frequent_itemsets[frequent_itemsets['length'] == 3])

            # Buat rules
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

            if rules.empty:
                st.warning("⚠️ Tidak ada aturan yang memenuhi nilai confidence.")
                return

            # Format tampilannya
            rules['support (%)'] = (rules['support'] * 100).round(2)
            rules['confidence (%)'] = (rules['confidence'] * 100).round(2)
            rules['lift'] = rules['lift'].round(2)
            rules = rules.sort_values(by='confidence', ascending=False)

            st.session_state['hasil_itemsets'] = frequent_itemsets
            st.session_state['hasil_rules'] = rules

            st.success("✅ Proses Apriori berhasil!")
            st.session_state['page'] = "Hasil"

        except Exception as e:
            st.error(f"Terjadi error saat proses Apriori: {e}")
