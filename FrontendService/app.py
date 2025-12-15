import streamlit as st

st.set_page_config(
    page_title="Bilabonnement Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from utils.style_loader import load_global_css
from components.ui_components import render_header, render_footer

from pages.cars_page import cars_page
from pages.customer_page import customers_page
from pages.contracts_page import contracts_page
from pages.dashboard_page import dashboard_page
from pages.ai_damage_page import ai_damage_page
from pages.login_page import login_page

load_global_css()

# Router init
if "page" not in st.session_state:
    st.session_state.page = "Login" if not st.session_state.get("jwt") else "Dashboard"

if not st.session_state.get("jwt") and st.session_state.page != "Login":
    st.session_state.page = "Login"


render_header(st.session_state.page)

if st.session_state.page == "Login":
    login_page()

elif st.session_state.page == "Dashboard":
    dashboard_page()

elif st.session_state.page == "Cars":
    cars_page()

elif st.session_state.page == "Customers":
    customers_page()

elif st.session_state.page == "Contracts":
    contracts_page()

elif st.session_state.page == "AI Damage":
    ai_damage_page()

if st.session_state.get("jwt") and st.session_state.page != "Login":
    render_footer()