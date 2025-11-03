import streamlit as st
from PIL import Image

def login_page():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("💬 Informasi")
        st.markdown("**Selamat datang di Sistem Apriori**")
        try:
            image = Image.open("assets/logo1.jpg")
            st.image(image, caption="", use_container_width=True)
        except:
            st.info("Logo tidak ditemukan.")

    with col2:
        st.subheader("🔐 Login Form")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if "admins" not in st.session_state:
                st.session_state["admins"] = {"admin": "fio"}  # default admin

            if username in st.session_state["admins"] and st.session_state["admins"][username] == password:
                st.session_state["login"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Username atau Password salah.")

    st.markdown('<div class="footer">© 2025 - Aplikasi Apriori</div>', unsafe_allow_html=True)
