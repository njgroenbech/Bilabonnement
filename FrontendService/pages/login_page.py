# FrontendService/pages/login_page.py
import requests
import streamlit as st
from components.ui_components import render_page_header
from utils.jwt_utils import get_role_from_jwt, get_username_from_jwt

AUTH_URL = "http://gateway:5001/auth/login"

def login_page():
    render_page_header("Login", "Log ind for at bruge dashboardet")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="admin / employee")
        password = st.text_input("Password", type="password", placeholder="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)

    if submitted:
        resp = requests.post(AUTH_URL, json={"username": username, "password": password}, timeout=10)
        

        if resp.status_code != 200:
            st.error(f"Login failed: {resp.text}")
            return

        data = resp.json()
        token = data.get("JWT_token")

        if not token:
            st.error("JWT_token is missing")
            return

        st.session_state.jwt = token
        st.session_state.role = get_role_from_jwt(token)
        st.session_state.username = get_username_from_jwt(token)
        st.session_state.page = "Dashboard"
        st.rerun()
