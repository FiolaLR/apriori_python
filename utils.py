import streamlit as st

def load_css():
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f8f9fa;
    }

    .header {
        background: linear-gradient(90deg, #0B2447, #19376D);
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 26px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .footer {
        position: fixed;
        left: 0; bottom: 0;
        width: 100%;
        background-color: #ddd;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

def header_footer():
    st.markdown('<div class="header">Aplikasi Apriori</div>', unsafe_allow_html=True)
