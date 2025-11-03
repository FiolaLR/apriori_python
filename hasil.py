import streamlit as st
import matplotlib.pyplot as plt

def hasil():
    st.subheader("📈 Hasil Apriori")

    if 'hasil_rules' in st.session_state and 'hasil_itemsets' in st.session_state:
        rules = st.session_state['hasil_rules']
        itemsets = st.session_state['hasil_itemsets']

        st.info(f"📊 Jumlah aturan yang terbentuk: **{len(rules)} rules**")
        st.info(f"📦 Jumlah frequent itemsets: **{len(itemsets)} itemsets**")

        def set_to_str(s):
            if isinstance(s, (set, frozenset)):
                return ', '.join(map(str, s))
            return str(s)

        # Pilihan jumlah kombinasi
        item_count = st.radio("Pilih jumlah item dalam kombinasi:", [2, 3])

        # Filter berdasarkan jumlah total item (antecedents + consequents)
        filtered_rules = rules[
            rules.apply(lambda r: len(r['antecedents']) + len(r['consequents']) == item_count, axis=1)
        ]

        # 🚨 Jika tidak ada hasil untuk item_count yang dipilih, fallback otomatis ke 2 item
        if filtered_rules.empty:
            if item_count == 3:
                st.warning("⚠️ Tidak ada aturan dengan 3 item. Menampilkan alternatif kombinasi 2 item.")
                filtered_rules = rules[
                    rules.apply(lambda r: len(r['antecedents']) + len(r['consequents']) == 2, axis=1)
                ]
            else:
                st.warning(f"Tidak ada aturan dengan {item_count} item.")

        # Jika masih ada hasil, tampilkan
        if not filtered_rules.empty:
            st.dataframe(
                filtered_rules[['antecedents', 'consequents', 'support (%)', 'confidence (%)', 'lift']],
                use_container_width=True
            )

            # 🔮 Rekomendasi warna-warni
            st.markdown("### 🔮 Rekomendasi Berdasarkan Aturan Apriori:")
            colors = ["#FFB6C1", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#DDA0DD"]

            for i, row in filtered_rules.iterrows():
                color = colors[i % len(colors)]
                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:8px;
                        font-size:16px;
                    ">
                        <b>Jika membeli</b> {', '.join(map(str, row['antecedents']))},
                        maka kemungkinan besar akan membeli
                        <b>{', '.join(map(str, row['consequents']))}</b>
                        (confidence: {row['confidence']:.2%})
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ⭐ Produk paling diminati
        if not itemsets.empty:
            top_item = itemsets.sort_values(by='support', ascending=False).iloc[0]
            st.info(
                f"⭐ **Produk paling banyak diminati:** {set_to_str(top_item['itemsets'])} "
                f"(support: {top_item['support']:.2%})"
            )

            # 📉 Produk kurang diminati (Planogram)
            st.subheader("📉 Produk Kurang Diminati (Planogram)")

            low_demand = itemsets.sort_values(by='support', ascending=True).head(5)
            st.dataframe(low_demand)

            # Visualisasi Planogram (bar chart)
            fig, ax = plt.subplots()
            ax.barh(low_demand['itemsets'].astype(str), low_demand['support'])
            ax.set_xlabel("Support")
            ax.set_title("Produk Kurang Diminati")
            st.pyplot(fig)

            # 🧭 Tingkat Kedekatan Antar Barang
            st.subheader("🧭 Tingkat Kedekatan Antar Barang")

            kedekatan = rules[['antecedents', 'consequents', 'lift']].copy()
            kedekatan['antecedents'] = kedekatan['antecedents'].apply(lambda x: list(x)[0])
            kedekatan['consequents'] = kedekatan['consequents'].apply(lambda x: list(x)[0])

            st.dataframe(kedekatan.sort_values(by='lift', ascending=False))

    else:
        st.info("Belum ada hasil Apriori. Silakan lakukan proses Apriori dulu.")
