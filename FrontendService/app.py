import streamlit as st
from api.api_client import api_get
from components.ui_components import (
    display_metric_card,
    display_status_badge,
    render_header,
    render_footer,
    render_page_header,
)
from pages.cars_page import cars_page
from pages.customer_page import customers_page
from pages.contracts_page import contracts_page

# Page Configuration
st.set_page_config(
    page_title="Bilabonnement Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    header[data-testid="stHeader"],
    [data-testid="stAppViewContainer"] > header {
        display: none !important;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 100% !important;
    }
    
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    h1 {
        color: #0f172a;
        font-weight: 800;
        font-size: 2.2rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0rem !important;
        padding-bottom: 0 !important;
    }
    
    .header-subtitle {
        color: #64748b; 
        font-size: 1rem; 
        margin-top: 0.25rem !important; 
        margin-bottom: 1.5rem !important;
        font-weight: 400;
    }
    
    h2 {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.2rem !important;
        margin-top: 1.5rem !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        padding: 2rem;
        border-radius: 24px;
        color: white;
        box-shadow: 0 10px 40px rgba(14, 165, 233, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50%;
        background: linear-gradient(180deg, rgba(255,255,255,0.15) 0%, transparent 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.4);
    }
    
    .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.95;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .status-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .status-card:hover {
        border-color: #0ea5e9;
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.2);
        transform: translateY(-3px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
        letter-spacing: 0.02em;
        min-height: 45px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #0284c7 0%, #0891b2 100%) !important;
    }
    
    .stButton > button:focus {
        border: 2px solid #0c4a6e !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.5) !important;
    }

    [data-testid="stTabs"] > div[role="tablist"] {
        background: #f8fafc;
        padding: 0.35rem;
        border-radius: 999px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 999px !important;
        border: none !important;
        color: #64748b;
        font-weight: 500;
        padding: 0.3rem 1rem;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        background: #ffffff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }

    [data-testid="stExpander"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        overflow: hidden;
    }

    [data-testid="stExpander"] > details > summary {
        background: #f8fafc !important;
        color: #0f172a !important;
    }

    [data-testid="stExpander"] > details > div {
        background: #ffffff !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
        overflow: hidden !important;
    }

    [data-testid="stDataFrame"] [role="grid"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    [data-testid="stDataFrame"] [role="row"] {
        background-color: #ffffff !important;
    }

    [data-testid="stDataFrame"] [role="row"]:nth-child(even) {
        background-color: #f8fafc !important;
    }

    [data-testid="stDataFrame"] [role="columnheader"] {
        background-color: #e5f2ff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        border-bottom: 1px solid #dbe2f0 !important;
    }

    [data-testid="stDataFrame"] [role="gridcell"] {
        border-color: #e5e7eb !important;
    }

    [data-testid="stDataFrame"] [role="row"]:hover {
        background-color: #e0f2fe !important;
    }

    .dataframe {
        border: none !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
        background: #ffffff !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .footer-info {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e2e8f0;
        padding: 1rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #64748b;
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def dashboard_page():
    """Dashboard Overview Page"""
    render_page_header(
        "📊 Dashboard Overview",
        "Welcome to your car subscription management system",
    )

    # Fetch data
    cars, car_error = api_get("/cars")
    customers, customer_error = api_get("/customers")
    contracts, contract_error = api_get("/contracts")

    # Calculate metrics
    total_cars = len(cars) if cars and not car_error else 0
    total_customers = len(customers) if customers and not customer_error else 0
    total_contracts = len(contracts) if contracts and not contract_error else 0

    # Display metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric_card("Total Fleet", total_cars, "🚗")
    with col2:
        display_metric_card("Customers", total_customers, "👥")
    with col3:
        display_metric_card("Active Contracts", total_contracts, "📄")

    # Fleet Status Breakdown
    if cars and not car_error:
        st.markdown(
            """
            <div style="margin-top: 4rem;"> 
                <h2 style="
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #0f172a;
                    margin: 0 0 0.05rem 0;
                ">
                    🚗 Fleet Status Breakdown
                </h2>
                <p style="
                    color: #64748b;
                    margin: 0;
                    font-size: 1.0rem;
                ">
                    Current availability and status of your vehicles
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        available = sum(1 for car in cars if car.get("status") == "available")
        rented = sum(1 for car in cars if car.get("status") == "rented")
        maintenance = sum(1 for car in cars if car.get("status") == "maintenance")

        with col1:
            display_status_badge("Available", available, "#10b981")
        with col2:
            display_status_badge("Rented", rented, "#f59e0b")
        with col3:
            display_status_badge("Maintenance", maintenance, "#ef4444")
        with col4:
            utilization = round((rented / total_cars * 100) if total_cars > 0 else 0, 1)
            display_status_badge("Utilization", f"{utilization}%", "#0ea5e9")


# Main App Router
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

render_header(st.session_state.page)

if st.session_state.page == "Dashboard":
    dashboard_page()
elif st.session_state.page == "Cars":
    cars_page()
elif st.session_state.page == "Customers":
    customers_page()
elif st.session_state.page == "Contracts":
    contracts_page()

render_footer()