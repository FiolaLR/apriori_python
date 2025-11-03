import streamlit as st

def register_admin():
    st.subheader("👑 Tambah Admin Baru")

    if "username" not in st.session_state or st.session_state.get("username") != "admin":
        st.warning("⚠️ Hanya admin utama yang bisa menambah admin baru.")
        return

    nama = st.text_input("Nama Lengkap")
    jabatan = st.text_input("Jabatan")
    new_admin = st.text_input("Username admin baru")
    new_password = st.text_input("Password admin baru", type="password")

    if st.button("Tambah Admin"):
        if not nama or not jabatan or not new_admin or not new_password:
            st.error("Semua field wajib diisi!")
        else:
            if "admins" not in st.session_state:
                st.session_state["admins"] = {"admin": "fio"}  # default admin

            if new_admin in st.session_state["admins"]:
                st.error("❌ Username sudah ada.")
            else:
                st.session_state["admins"][new_admin] = new_password
                st.success(f"✅ Admin **{nama}** (username: {new_admin}) berhasil ditambahkan!")

    st.markdown('<div class="footer">© 2025 - Aplikasi Apriori</div>', unsafe_allow_html=True)
