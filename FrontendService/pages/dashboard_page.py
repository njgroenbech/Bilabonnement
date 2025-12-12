import streamlit as st
from api.api_client import api_get
from components.ui_components import (
    display_metric_card,
    display_status_badge,
    render_page_header,
)

# Dashboard Overview Page
def dashboard_page():
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