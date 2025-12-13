import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bilabonnement Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Imports
from utils.style_loader import load_global_css
from components.ui_components import (
    render_header,
    render_footer,
)
from pages.cars_page import cars_page
from pages.customer_page import customers_page
from pages.contracts_page import contracts_page
from pages.dashboard_page import dashboard_page
from pages.ai_damage_page import ai_damage_page

# Load Global CSS
load_global_css()

# Session State (Router)
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Layout
render_header(st.session_state.page)

if st.session_state.page == "Dashboard":
    dashboard_page()

elif st.session_state.page == "Cars":
    cars_page()

elif st.session_state.page == "Customers":
    customers_page()

elif st.session_state.page == "Contracts":
    contracts_page()
    
elif st.session_state.page == "AI Damage":
    ai_damage_page()
render_footer()