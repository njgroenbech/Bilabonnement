import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dateutil import parser
from api.api_client import api_get
from components.ui_components import (
    display_metric_card,
    display_status_badge,
    render_page_header,
)

# Helper functions for data processing and visualization
def _parse_contracts_for_revenue(contracts):
    parsed = []
    for contract in contracts:
        if contract.get("start_date") and contract.get("sub_price_per_month", 0) > 0:
            parsed.append({
                "start": parser.parse(contract["start_date"]).replace(tzinfo=None, day=1),
                "revenue": contract["sub_price_per_month"],
            })
    return parsed

# Generate monthly data for the last 6 months
def _generate_monthly_data(parsed_contracts):
    if not parsed_contracts:
        return []
    
    earliest_date = min(c["start"] for c in parsed_contracts)
    current_month = earliest_date
    now = datetime.now().replace(tzinfo=None, day=1)
    months_data = []

    while current_month <= now:
        monthly_revenue = sum(
            c["revenue"] for c in parsed_contracts 
            if c["start"] <= current_month
        )
        months_data.append({
            "Month": current_month.strftime("%b %Y"),
            "Revenue": monthly_revenue
        })
        
        # Move to next month
        current_month = (
            current_month.replace(year=current_month.year + 1, month=1)
            if current_month.month == 12
            else current_month.replace(month=current_month.month + 1)
        )

    return months_data[-6:]  # Keep only last 6 months

# Create monthly revenue line chart
def create_monthly_revenue_line_chart(contracts):
    if not contracts:
        return None

    parsed_contracts = _parse_contracts_for_revenue(contracts)
    months_data = _generate_monthly_data(parsed_contracts)
    
    if not months_data:
        return None

    df = pd.DataFrame(months_data)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Month"],
        y=df["Revenue"],
        mode="lines+markers",
        name="Monthly Revenue",
        line=dict(color="#0ea5e9", width=3),
        marker=dict(size=10, color="#0ea5e9"),
        fill="tozeroy",
        fillcolor="rgba(14, 165, 233, 0.1)"
    ))

    fig.update_layout(
        title="Monthly Revenue Trend",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(
            title="Month",
            showgrid=False,
            showline=True,
            linecolor="#e5e7eb",
        ),
        yaxis=dict(
            title="Revenue (kr)",
            showgrid=True,
            gridcolor="#f3f4f6",
        ),
        margin=dict(t=50, b=20, l=20, r=20),
        height=400,
        hovermode="x unified",
        showlegend=False
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Revenue: %{y:,.0f} kr<extra></extra>"
    )

    return fig

# Create brand revenue bar chart
def create_brand_revenue_bar_chart(active_contracts, cars):
    if not active_contracts or not cars:
        return None

    car_lookup = {
        car["car_id"]: car["brand"]
        for car in cars
        if "car_id" in car and "brand" in car
    }

    brand_data = {}
    for contract in active_contracts:
        brand = car_lookup.get(contract.get("car_id"))
        revenue = contract.get("sub_price_per_month", 0)

        if brand:
            if brand not in brand_data:
                brand_data[brand] = {"revenue": 0, "count": 0}
            brand_data[brand]["revenue"] += revenue
            brand_data[brand]["count"] += 1

    if not brand_data:
        return None

    df = pd.DataFrame([
        {
            "Brand": brand,
            "Revenue": data["revenue"],
            "Cars Rented": data["count"]
        }
        for brand, data in brand_data.items()
    ]).sort_values("Revenue", ascending=False)

    fig = px.bar(
        df,
        x="Brand",
        y="Revenue",
        title="Revenue by Car Brand",
        color="Revenue",
        color_continuous_scale=["#10b981", "#059669"],
        text="Revenue",
    )

    fig.update_layout(coloraxis_showscale=False)

    fig.update_traces(
        texttemplate="%{text:,.0f} kr",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Revenue: %{y:,.0f} kr<br>Cars Rented: %{customdata[0]}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f3f4f6"),
        height=450,
    )

    return fig

# Render section header
def _render_section_header(emoji, title, subtitle):
    st.markdown(
        f"""
        <div style="margin-top: 4rem;"> 
            <h2 style="font-size: 1.8rem; font-weight: 700;">
                {emoji} {title}
            </h2>
            <p style="color: #64748b;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Dashboard Page
def dashboard_page():
    render_page_header(
        "📊 Dashboard Overview",
        "Welcome to your car subscription management system",
    )

    # Fetch data from microservices
    cars, car_error = api_get("/cars")
    customers, customer_error = api_get("/customers")
    contracts, contract_error = api_get("/contracts")

    cars = cars or []
    customers = customers or []
    contracts = contracts or []

    # KPI Metrics
    total_cars = len(cars)
    total_customers = len(customers)
    active_contracts = [c for c in contracts if c.get("status") == "active"]
    total_active_contracts = len(active_contracts)

    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric_card("Total Fleet", total_cars, "🚗")
    with col2:
        display_metric_card("Customers", total_customers, "👥")
    with col3:
        display_metric_card("Active Contracts", total_active_contracts, "📄")

    # Fleet Status Breakdown
    if cars:
        _render_section_header(
            "🚗",
            "Fleet Status Breakdown",
            "Current availability and status of your vehicles"
        )

        available = sum(1 for car in cars if car.get("status") == "available")
        rented = sum(1 for car in cars if car.get("status") == "rented")
        maintenance = sum(1 for car in cars if car.get("status") == "maintenance")
        utilization = round((rented / total_cars * 100) if total_cars else 0, 1)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            display_status_badge("Available", available, "#10b981")
        with col2:
            display_status_badge("Rented", rented, "#f59e0b")
        with col3:
            display_status_badge("Maintenance", maintenance, "#ef4444")
        with col4:
            display_status_badge("Utilization", f"{utilization}%", "#0ea5e9")

    role = st.session_state.get("role")

    if role != "admin":
        st.stop()

    # Key Business Insights Section
    _render_section_header(
        "📈",
        "Key Business Insights",
        "Revenue trends and performance by car brand"
    )

    if not contracts:
        st.info("No contracts available for analysis.")
        return

    # Graph 1: Monthly Revenue Line Chart
    fig_revenue_trend = create_monthly_revenue_line_chart(contracts)
    if fig_revenue_trend:
        st.plotly_chart(fig_revenue_trend, use_container_width=True)
    else:
        st.info("No revenue data available.")

    # Graph 2: Brand Revenue Bar Chart
    if active_contracts:
        fig_brand_revenue = create_brand_revenue_bar_chart(active_contracts, cars)
        if fig_brand_revenue:
            st.plotly_chart(fig_brand_revenue, use_container_width=True)
        else:
            st.info("No brand revenue data available.")
    else:
        st.info("No active contracts available for brand analysis.")