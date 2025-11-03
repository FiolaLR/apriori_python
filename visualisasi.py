import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

def visualisasi():
    st.subheader("📊 Visualisasi Hasil Apriori")

    if 'hasil_itemsets' not in st.session_state or 'hasil_rules' not in st.session_state:
        st.warning("⚠️ Belum ada hasil Apriori. Silakan jalankan proses Apriori terlebih dahulu.")
        return

    itemsets = st.session_state['hasil_itemsets']
    rules = st.session_state['hasil_rules']

    # --- Produk Paling Diminati ---
    st.subheader("📊 Produk Paling Diminati")
    top_items = itemsets.sort_values(by='support', ascending=False).head(10)
    fig1, ax1 = plt.subplots()
    ax1.barh(top_items['itemsets'].astype(str), top_items['support'], color='skyblue')
    ax1.set_xlabel("Support")
    ax1.set_title("10 Produk Paling Diminati")
    st.pyplot(fig1)

    # --- Produk Kurang Diminati ---
    st.subheader("📉 Produk Kurang Diminati (Planogram)")
    low_items = itemsets.sort_values(by='support', ascending=True).head(10)
    fig2, ax2 = plt.subplots()
    ax2.barh(low_items['itemsets'].astype(str), low_items['support'], color='salmon')
    ax2.set_xlabel("Support")
    ax2.set_title("10 Produk Kurang Diminati")
    st.pyplot(fig2)

    # --- Hubungan Support vs Confidence ---
    st.subheader("📈 Hubungan Support vs Confidence")
    fig3, ax3 = plt.subplots()
    ax3.scatter(rules['support'], rules['confidence'], s=rules['lift']*10, alpha=0.6)
    ax3.set_xlabel("Support")
    ax3.set_ylabel("Confidence")
    ax3.set_title("Hubungan Support vs Confidence (Ukuran = Lift)")
    st.pyplot(fig3)

    # --- Graph Hubungan Produk ---
    st.subheader("🕸️ Jaringan Hubungan Antar Produk (Graph)")

    import networkx as nx
    G = nx.DiGraph()

    for _, row in rules.iterrows():
        for a in row['antecedents']:
            for c in row['consequents']:
                G.add_edge(a, c, weight=row['lift'])

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="lightblue",
            arrowsize=20, font_size=8, ax=ax4)
    st.pyplot(fig4)
