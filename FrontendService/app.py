import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

GATEWAY_URL = "http://api_gateway:5001"

# Page configuration
st.set_page_config(
    page_title="Bilabonnement Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global CSS / theming
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

    /* TABS (Cars / Customers / Contracts undersider)                 */
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

    /* EXPANDER (Filter Options på Cars-siden)                        */
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

    /* Fjern den mørke kant rundt om expander indhold */
    [data-testid="stExpander"] > details > div {
        background: #ffffff !important;
    }

    /* DATAFRAME (tabeller på Cars / Customers / Contracts)           */
    /* Wrapper */
    [data-testid="stDataFrame"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08) !important;
        overflow: hidden !important;
    }

    /* Selve tabellen */
    [data-testid="stDataFrame"] [role="grid"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    /* Rækker */
    [data-testid="stDataFrame"] [role="row"] {
        background-color: #ffffff !important;
    }

    [data-testid="stDataFrame"] [role="row"]:nth-child(even) {
        background-color: #f8fafc !important;
    }

    /* Kolonne-headere */
    [data-testid="stDataFrame"] [role="columnheader"] {
        background-color: #e5f2ff !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        border-bottom: 1px solid #dbe2f0 !important;
    }

    /* Celler */
    [data-testid="stDataFrame"] [role="gridcell"] {
        border-color: #e5e7eb !important;
    }

    [data-testid="stDataFrame"] [role="row"]:hover {
        background-color: #e0f2fe !important;
    }

    /* Styling hvis pandas selv renderer en HTML-table */
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

# Helper functions
def api_get(endpoint: str):
    try:
        r = requests.get(f"{GATEWAY_URL}{endpoint}", timeout=5)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Error: {r.status_code} - {r.text}"
    except Exception as e:
        return None, str(e)

def api_post(endpoint: str, data: dict):
    try:
        r = requests.post(f"{GATEWAY_URL}{endpoint}", json=data, timeout=5)
        if r.status_code in (200, 201):
            return r.json(), None
        return None, f"Error: {r.status_code} - {r.text}"
    except Exception as e:
        return None, str(e)

def display_metric_card(title: str, value, icon: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{icon} {title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_status_badge(label: str, value, color: str = "#0ea5e9"):
    st.markdown(
        f"""
        <div class="status-card">
            <p style="margin: 0; color: #475569; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">{label}</p>
            <p style="margin: 0.5rem 0 0 0; color: {color}; font-size: 2rem; font-weight: 800; line-height: 1;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_page_header(title: str, subtitle: str):
    """Ensartet overskrift + undertekst på alle sider."""
    st.markdown(
        f"""
        <h1 style='color: #0f172a; font-weight: 800; font-size: 2rem; margin: 0;'>{title}</h1>
        <p class='header-subtitle'>{subtitle}</p>
        """,
        unsafe_allow_html=True,
    )

def api_delete(endpoint: str):
    try:
        r = requests.delete(f"{GATEWAY_URL}{endpoint}", timeout=5)
        if r.status_code in (200, 204):
            return True, None
        return False, f"Error: {r.status_code} - {r.text}"
    except Exception as e:
        return False, str(e)
    
# Navigation Header
def render_header(current_page: str):
    col_logo, col_home, col_spacer, col_nav1, col_nav2, col_nav3 = st.columns([2.1, 0.5, 4.5, 1.2, 1.2, 1.2])
    
    with col_logo:
        try:
            st.image("Bilabonnement.svg", width=350)
        except Exception:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="font-size: 2rem;">🚗</div>
                    <div>
                        <h2 style="margin: 0; color: #0ea5e9; font-size: 1.4rem;">BILABONNEMENT</h2>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
    with col_home:
        if st.button(
            "🏠",
            use_container_width=True,
            type="primary" if current_page == "Dashboard" else "secondary",
            help="Dashboard",
            key="home_btn"
        ):
            st.session_state.page = "Dashboard"
            st.rerun()

    # col_spacer er tom

    with col_nav1:
        if st.button(
            "🚗 Cars",
            use_container_width=True,
            type="primary" if current_page == "Cars" else "secondary",
        ):
            st.session_state.page = "Cars"
            st.rerun()
            
    with col_nav2:
        if st.button(
            "👥 Customers",
            use_container_width=True,
            type="primary" if current_page == "Customers" else "secondary",
        ):
            st.session_state.page = "Customers"
            st.rerun()
            
    with col_nav3:
        if st.button(
            "📄 Contracts",
            use_container_width=True,
            type="primary" if current_page == "Contracts" else "secondary",
        ):
            st.session_state.page = "Contracts"
            st.rerun()
    
    st.markdown(
        "<hr style='margin: 0.5rem 0 1.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>",
        unsafe_allow_html=True,
    )

# Footer
def render_footer():
    st.markdown(
        """
        <div class="footer-info">
            <div>
                <span style="font-weight: 600; color: #1e293b;">Bilabonnement Dashboard</span>
                <span style="margin-left: 1rem;">Version 1.0.0</span>
            </div>
            <div>
                <span style="margin-right: 1.5rem;">Status: <span style="color: #10b981;">● Online</span></span>
                <span>Gateway: <span style="color: #10b981;">Active</span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Pages
def dashboard_page():
    render_page_header(
        "📊 Dashboard Overview",
        "Welcome to your car subscription management system",
    )

    cars, car_error = api_get("/cars")
    customers, customer_error = api_get("/customers")
    contracts, contract_error = api_get("/contracts")

    has_cars = cars and not car_error
    has_customers = customers and not customer_error
    has_contracts = contracts and not contract_error

    total_cars = len(cars) if has_cars else 0
    total_customers = len(customers) if has_customers else 0
    total_contracts = len(contracts) if has_contracts else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric_card("Total Fleet", total_cars, "🚗")
    with col2:
        display_metric_card("Customers", total_customers, "👥")
    with col3:
        display_metric_card("Active Contracts", total_contracts, "📄")

    if has_cars:
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
                    margin: 4;
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

def cars_page():
    render_page_header(
        "🚗 Car Fleet Management", "Manage your complete vehicle inventory"
    )

    tab1, tab2 = st.tabs(["📋 All Vehicles", "➕ Add New Vehicle"])

    # ---- TAB 1: LISTE ----
    with tab1:
        cars, error = api_get("/cars")
        if error:
            st.error(f"❌ {error}")
        elif cars:
            df = pd.DataFrame(cars)

            with st.expander("🔍 Filter Options", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_filter = st.multiselect(
                        "Status",
                        options=["available", "rented", "maintenance"],
                        default=["available", "rented", "maintenance"],
                    )
                with col2:
                    if "brand" in df.columns:
                        brands = ["All"] + sorted(df["brand"].unique().tolist())
                        brand_filter = st.selectbox("Brand", brands)
                    else:
                        brand_filter = None
                with col3:
                    if "fuel_type" in df.columns:
                        fuel_types = ["All"] + sorted(df["fuel_type"].unique().tolist())
                        fuel_filter = st.selectbox("Fuel Type", fuel_types)
                    else:
                        fuel_filter = None

            if status_filter and "status" in df.columns:
                df = df[df["status"].isin(status_filter)]
            if brand_filter and brand_filter != "All" and "brand" in df.columns:
                df = df[df["brand"] == brand_filter]
            if fuel_filter and fuel_filter != "All" and "fuel_type" in df.columns:
                df = df[df["fuel_type"] == fuel_filter]

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Showing <strong>{len(df)}</strong> vehicles</p>",
                unsafe_allow_html=True,
            )
            
            # Vis dataframe
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                height=400,
                disabled=df.columns.tolist(),
                num_rows="fixed",
                key="car_table"
            )

            # Delete sektion under tabellen
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col2:
                # Dropdown til at vælge car til sletning
                car_options = {
                    f"{c['brand']} {c['model']} - {c['license_plate']}": c['car_id']
                    for c in cars
                }
                
                selected_to_delete = st.selectbox(
                    "Select vehicle to delete:",
                    options=[""] + list(car_options.keys()),
                    format_func=lambda x: "Select a vehicle..." if x == "" else x,
                    key="car_delete_select"
                )
                
                if selected_to_delete and selected_to_delete != "":
                    car_id = car_options[selected_to_delete]
                    
                    if st.button(
                        "🗑️ Delete Selected Vehicle",
                        type="primary",
                        use_container_width=True,
                        key="car_delete_btn"
                    ):
                        with st.spinner("Deleting vehicle..."):
                            _, err = api_delete(f"/cars/{car_id}")
                            if err:
                                st.error(f"❌ Failed to delete: {err}")
                            else:
                                st.success(f"✅ Vehicle deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()
        else:
            st.info(
                "ℹ️ No vehicles found in the fleet. Add your first vehicle to get started!"
            )

    # ---- TAB 2: NY BIL ----
    with tab2:
        with st.form("add_car_form", clear_on_submit=True):
            st.markdown("### 🚘 Vehicle Details")

            col1, col2, col3 = st.columns(3)
            with col1:
                brand = st.text_input("Brand *", placeholder="Toyota, BMW, Tesla...")
                model = st.text_input("Model *", placeholder="Camry, X5, Model 3...")
                year = st.number_input(
                    "Year *", min_value=1990, max_value=2030, value=2024
                )
            with col2:
                license_plate = st.text_input("License Plate *", placeholder="AB12345")
                km_driven = st.number_input(
                    "Kilometers Driven *", min_value=0, value=0, step=1000
                )
                fuel_type = st.selectbox(
                    "Fuel Type *",
                    ["Petrol", "Diesel", "Electric", "Hybrid"],
                )
            with col3:
                status = st.selectbox(
                    "Status *", ["available", "rented", "maintenance"]
                )
                purchase_price = st.number_input(
                    "Purchase Price (DKK) *", min_value=0, value=0, step=10000
                )
                sub_price_per_month = st.number_input(
                    "Subscription price per month (DKK) *",
                    min_value=0,
                    value=0,
                    step=500,
                )
                location = st.text_input(
                    "Location *", placeholder="Copenhagen, Aarhus..."
                )

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                submitted = st.form_submit_button(
                    "🚀 Add Vehicle to Fleet", use_container_width=True
                )

            if submitted:
                if not all([brand, model, license_plate, location]):
                    st.error("❌ Please fill in all required fields marked with *")
                else:
                    new_car = {
                        "brand": brand,
                        "model": model,
                        "year": int(year),
                        "license_plate": license_plate,
                        "km_driven": int(km_driven),
                        "fuel_type": fuel_type.lower(),
                        "status": status,
                        "purchase_price": int(purchase_price),
                        "sub_price_per_month": int(sub_price_per_month),
                        "location": location,
                    }
                    _, error = api_post("/cars", new_car)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"✅ Successfully added {brand} {model} to the fleet!")
                        st.balloons()

def customers_page():
    render_page_header(
        "👥 Customer Management", "Manage your customer database"
    )

    tab1, tab2 = st.tabs(["📋 All Customers", "➕ New Customer"])

    with tab1:
        customers, error = api_get("/customers")
        contracts, _ = api_get("/contracts")
        
        if error:
            st.error(f"❌ {error}")
        elif customers:
            df = pd.DataFrame(customers)
            
            # Find customers with active contracts
            active_customer_ids = []
            if contracts:
                active_customer_ids = [
                    c['customer_id'] for c in contracts 
                    if c.get('status') == 'active'
                ]
            
            # Tilføj kolonne til dataframe
            df['has_active_contract'] = df['customer_id'].isin(active_customer_ids)

            # Filter options
            col1, col2 = st.columns([3, 1])
            with col1:
                search = st.text_input(
                    "🔍 Search customers",
                    placeholder="Search by name, email, or CPR number...",
                )
            with col2:
                filter_option = st.selectbox(
                    "Filter",
                    ["All Customers", "Active Contracts", "Available"],
                    key="customer_filter"
                )
            
            # Apply search filter
            if search:
                search_lower = search.lower()
                mask = df.apply(
                    lambda row: row.astype(str)
                    .str.lower()
                    .str.contains(search_lower)
                    .any(),
                    axis=1,
                )
                df = df[mask]
            
            # Apply contract status filter
            if filter_option == "Active Contracts":
                df = df[df['has_active_contract'] == True]
            elif filter_option == "Available":
                df = df[df['has_active_contract'] == False]

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Showing <strong>{len(df)}</strong> customers</p>",
                unsafe_allow_html=True,
            )
            
            # Vis dataframe
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                height=400,
                disabled=df.columns.tolist(),
                num_rows="fixed",
                key="customer_table"
            )

            # Delete sektion under tabellen
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col2:
                # Dropdown til at vælge customer til sletning
                customer_options = {
                    f"{c['name']} {c['last_name']} - {c['email']}": c['customer_id']
                    for c in customers
                }
                
                selected_to_delete = st.selectbox(
                    "Select customer to delete:",
                    options=[""] + list(customer_options.keys()),
                    format_func=lambda x: "Select a customer..." if x == "" else x,
                    key="customer_delete_select"
                )
                
                if selected_to_delete and selected_to_delete != "":
                    customer_id = customer_options[selected_to_delete]
                    
                    if st.button(
                        "🗑️ Delete Selected Customer",
                        type="primary",
                        use_container_width=True,
                        key="customer_delete_btn"
                    ):
                        with st.spinner("Deleting customer..."):
                            _, err = api_delete(f"/customers/{customer_id}")
                            if err:
                                st.error(f"❌ Failed to delete: {err}")
                            else:
                                st.success(f"✅ Customer deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()
        else:
            st.info("ℹ️ No customers found. Add your first customer to get started!")

    with tab2:
        with st.form("add_customer_form", clear_on_submit=True):
            st.markdown("### 👤 Personal Information")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("First Name *", placeholder="John")
                last_name = st.text_input("Last Name *", placeholder="Doe")
                email = st.text_input("Email *", placeholder="john.doe@example.com")
                cpr_number = st.text_input(
                    "CPR Number *", placeholder="DDMMYY-XXXX"
                )
            with col2:
                address = st.text_input(
                    "Address *", placeholder="Vestergade 10, 2. th"
                )
                postal_code = st.text_input("Postal Code *", placeholder="1000")
                city = st.text_input("City *", placeholder="Copenhagen")

            st.markdown("### 💳 Banking Information")
            col3, col4 = st.columns(2)
            with col3:
                registration_number = st.text_input(
                    "Registration Number", placeholder="1234"
                )
                account_number = st.text_input(
                    "Account Number", placeholder="1234567890"
                )
            with col4:
                comments = st.text_area(
                    "Notes",
                    placeholder="Additional information about the customer...",
                    height=100,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                submitted = st.form_submit_button(
                    "✨ Create Customer Profile", use_container_width=True
                )

            if submitted:
                if not all(
                    [name, last_name, email, cpr_number, address, postal_code, city]
                ):
                    st.error("❌ Please fill in all required fields marked with *")
                else:
                    new_customer = {
                        "name": name,
                        "last_name": last_name,
                        "address": address,
                        "postal_code": postal_code,
                        "city": city,
                        "email": email,
                        "cpr_number": cpr_number,
                        "registration_number": registration_number,
                        "account_number": account_number,
                        "comments": comments,
                    }
                    _, error = api_post("/customers", new_customer)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(
                            f"✅ Successfully created profile for {name} {last_name}!"
                        )
                        st.balloons()

def contracts_page():
    render_page_header(
        "📄 Contract Management",
        "Create and manage subscription contracts",
    )

    tab1, tab2 = st.tabs(["📋 All Contracts", "➕ New Contract"])

    # ======================================================
    # TAB 1 — ALL CONTRACTS
    # ======================================================
    with tab1:
        contracts, error = api_get("/contracts")

        if error:
            st.error(f"❌ {error}")

        elif contracts:
            df = pd.DataFrame(contracts)

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>"
                f"Showing <strong>{len(df)}</strong> contracts</p>",
                unsafe_allow_html=True,
            )

            # Vis dataframe
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                height=400,
                disabled=df.columns.tolist(),
                num_rows="fixed",
                key="contract_table"
            )

            # Delete sektion under tabellen
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col2:
                # Dropdown til at vælge contract til sletning
                contract_options = {
                    f"Contract #{c['contract_id']} - Customer #{c.get('customer_id', 'N/A')}": c['contract_id']
                    for c in contracts
                }
                
                selected_to_delete = st.selectbox(
                    "Select contract to delete:",
                    options=[""] + list(contract_options.keys()),
                    format_func=lambda x: "Select a contract..." if x == "" else x,
                    key="contract_delete_select"
                )
                
                if selected_to_delete and selected_to_delete != "":
                    contract_id = contract_options[selected_to_delete]
                    
                    if st.button(
                        "🗑️ Delete Selected Contract",
                        type="primary",
                        use_container_width=True,
                        key="contract_delete_btn"
                    ):
                        with st.spinner("Deleting contract..."):
                            _, err = api_delete(f"/contracts/{contract_id}")
                            if err:
                                st.error(f"❌ Failed to delete: {err}")
                            else:
                                st.success(f"✅ Contract deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()

        else:
            st.info("ℹ️ No contracts found. Create your first contract to get started!")

    # ======================================================
    # TAB 2 — NEW CONTRACT
    # ======================================================
    with tab2:
        st.markdown("### 📝 Create New Contract")

        # ---------- LOAD CUSTOMERS ----------
        customers, cust_error = api_get("/customers")
        contracts, _ = api_get("/contracts")
        
        if cust_error:
            st.error("❌ Failed to load customers")
            return

        if not customers:
            st.warning("⚠ No customers exist. Create a customer before making a contract.")
            return

        # Filter out customers with active contracts
        active_customer_ids = []
        if contracts:
            active_customer_ids = [
                c['customer_id'] for c in contracts 
                if c.get('status') == 'active'
            ]
        
        available_customers = [
            c for c in customers 
            if c['customer_id'] not in active_customer_ids
        ]

        if not available_customers:
            st.warning("⚠ No available customers. All customers already have active contracts.")
            st.info("💡 Tip: Delete an existing contract or add a new customer to create a contract.")
            return

        customer_options = {
            f"{c['name']} {c['last_name']} ({c['email']})": c
            for c in available_customers
        }

        selected_customer = st.selectbox(
            "👤 Select Customer *",
            list(customer_options.keys())
        )
        customer = customer_options[selected_customer]

        # ---------- LOAD CARS ----------
        cars, car_error = api_get("/cars")
        if car_error:
            st.error("❌ Failed to load cars")
            return

        available_cars = [c for c in cars if c.get("status") == "available"]

        if not available_cars:
            st.warning("⚠ No available cars. All cars are rented or under maintenance.")
            return

        car_options = {
            f"{c['brand']} {c['model']} – {c['license_plate']}": c
            for c in available_cars
        }

        selected_car = st.selectbox(
            "🚗 Select Available Car *",
            list(car_options.keys())
        )
        car = car_options[selected_car]

        # ---------- CONTRACT PERIOD ----------
        st.markdown("### 📅 Contract Period")
        col7, col8 = st.columns(2)

        with col7:
            start_date = st.date_input("Start Date *", value=datetime.now().date())
        with col8:
            end_date = st.date_input("End Date *", value=datetime.now().date())

        if start_date and end_date:
            duration = (end_date - start_date).days
            st.markdown(
                f"<p style='color: #0ea5e9; font-weight: 600; margin-top: 0.5rem;'>"
                f"Contract Duration: {duration} days ({duration // 30} months)"
                f"</p>",
                unsafe_allow_html=True,
            )

        # ---------- SUB PRICE (AUTO FROM CAR) ----------
        st.markdown("### 💰 Subscription Details")

        # Vis prisen fra bilen - ikke redigerbar
        sub_price_per_month = car.get('sub_price_per_month', 0)

        st.markdown(
            f"<p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>"
            f"Subscription price per month: <strong style='color: #0ea5e9;'>{sub_price_per_month:,} DKK</strong>"
            f"</p>",
            unsafe_allow_html=True
        )

        st.info(f"💡 This is the standard price for the {car['brand']} {car['model']}")

        # ---------- SUBMIT BUTTON ----------
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_btn, _ = st.columns([1, 1, 1])

        with col_btn:
            submitted = st.button("📝 Create Contract", use_container_width=True)

        if submitted:
            if start_date >= end_date:
                st.error("❌ End date must be after start date")
                return

            payload = {
                "customer_id": customer["customer_id"],
                "car_id": car["car_id"],
                "start_date": str(start_date),
                "end_date": str(end_date),
                "sub_price_per_month": int(sub_price_per_month),  # Brug bilens pris
            }

            _, error = api_post("/contracts", payload)

            if error:
                st.error(f"❌ {error}")
            else:
                st.success(
                    f"✅ Contract created for {customer['name']} {customer['last_name']} "
                    f"and {car['brand']} {car['model']} at {sub_price_per_month:,} DKK/month!"
                )
                st.balloons()

# Main app
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