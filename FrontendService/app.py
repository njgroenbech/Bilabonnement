import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

GATEWAY_URL = "http://api_gateway:5001"
DAMAGE_CHECK_URL = os.getenv(
    "DAMAGE_CHECK_URL",
    f"{GATEWAY_URL}/api/damage/check",
)

# Page configuration
st.set_page_config(
    page_title="Bilabonnement dashboard",
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
        border-radius: 10px;
        padding: 0.4rem 0.9rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.28);
        letter-spacing: 0.02em;
        min-height: 42px;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
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

# Helper functions
def api_get(endpoint: str):
    try:
        r = requests.get(f"{GATEWAY_URL}{endpoint}", timeout=5)
        if r.status_code == 200:
            return r.json(), None
        return None, f"Fejl {r.status_code}: {r.text}"
    except Exception as e:
        return None, f"Teknisk fejl ved kald til API: {e}"

def api_post(endpoint: str, data: dict):
    try:
        r = requests.post(f"{GATEWAY_URL}{endpoint}", json=data, timeout=5)
        if r.status_code in (200, 201):
            return r.json(), None
        return None, f"Fejl {r.status_code}: {r.text}"
    except Exception as e:
        return None, f"Teknisk fejl ved kald til API: {e}"

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

# Navigation Header
def render_header(current_page: str):
    col_logo, col_home, col_spacer, col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(
        [1.2, 0.45, 1.2, 1, 1, 1, 1]
    )

    with col_logo:
        try:
            st.image("Bilabonnement.svg", width=220)
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
            help="Startside",
            key="home_btn",
        ):
            st.session_state.page = "Dashboard"
            st.rerun()

    with col_nav1:
        if st.button(
            "🚗 Bilflåde",
            use_container_width=True,
            type="primary" if current_page == "Cars" else "secondary",
        ):
            st.session_state.page = "Cars"
            st.rerun()
            
    with col_nav2:
        if st.button(
            "👥 Kunder",
            use_container_width=True,
            type="primary" if current_page == "Customers" else "secondary",
        ):
            st.session_state.page = "Customers"
            st.rerun()
            
    with col_nav3:
        if st.button(
            "📄 Kontrakter",
            use_container_width=True,
            type="primary" if current_page == "Contracts" else "secondary",
        ):
            st.session_state.page = "Contracts"
            st.rerun()

    with col_nav4:
        if st.button(
            "🧠 Skadesvurdering",
            use_container_width=True,
            type="primary" if current_page == "AI Damage" else "secondary",
        ):
            st.session_state.page = "AI Damage"
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
                <span style="font-weight: 600; color: #1e293b;">Bilabonnement dashboard</span>
                <span style="margin-left: 1rem;">Version 1.0.0</span>
            </div>
            <div>
                <span style="margin-right: 1.5rem;">Status: <span style="color: #10b981;">● Online</span></span>
                <span>Gateway: <span style="color: #10b981;">Aktiv</span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Pages
def dashboard_page():
    render_page_header(
        "📊 Oversigt",
        "Velkommen til administrationssystemet for bilabonnementer.",
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
        display_metric_card("Samlet flåde", total_cars, "🚗")
    with col2:
        display_metric_card("Kunder", total_customers, "👥")
    with col3:
        display_metric_card("Aktive kontrakter", total_contracts, "📄")

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
                    🚗 Flådestatus
                </h2>
                <p style="
                    color: #64748b;
                    margin: 4;
                    font-size: 1.0rem;
                ">
                    Aktuel tilgængelighed og status for køretøjerne.
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
            display_status_badge("Tilgængelige", available, "#10b981")
        with col2:
            display_status_badge("Udlejede", rented, "#f59e0b")
        with col3:
            display_status_badge("Til service", maintenance, "#ef4444")
        with col4:
            utilization = round((rented / total_cars * 100) if total_cars > 0 else 0, 1)
            display_status_badge("Udnyttelse", f"{utilization}%", "#0ea5e9")

def ai_damage_page():
    render_page_header(
        "🧠 AI skadesvurdering",
        "Upload billeder af bilen og få en simuleret skadesvurdering.",
    )

    uploaded_files = st.file_uploader(
        "Vælg et eller flere billeder af bilen",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if st.button("Få vurdering"):
        if not uploaded_files:
            st.warning("Upload mindst ét billede, før du beder om vurdering.")
        else:
            with st.spinner("Sender billeder til AI-simulering..."):
                files = [
                    ("images", (f.name, f.getvalue(), f.type))
                    for f in uploaded_files
                ]

                try:
                    resp = requests.post(DAMAGE_CHECK_URL, files=files)
                except Exception as e:
                    st.error(f"Kunne ikke kontakte API-gateway: {e}")
                else:
                    if resp.status_code != 200:
                        st.error(f"Fejl fra backend: {resp.text}")
                    else:
                        data = resp.json()
                        status = data.get("overall_status")
                        color = data.get("color")
                        message = data.get("message", "")
                        damage_level = data.get("damage_level")

                        if status == "unclear":
                            st.warning(f"🟡 {message}")
                        elif status == "clear":
                            st.success(f"🟢 {message}")
                        elif status == "damage_found":
                            st.error(f"🔴 {message}")
                        else:
                            st.info(message or "Ukendt status fra AI-vurdering.")

def cars_page():
    render_page_header(
        "🚗 Bilflådehåndtering",
        "Administrér de biler, der indgår i abonnementsløsningen.",
    )

    tab1, tab2 = st.tabs(["📋 Alle køretøjer", "➕ Tilføj nyt køretøj"])

    with tab1:
        cars, error = api_get("/cars")
        if error:
            st.error(f"❌ {error}")
        elif cars:
            df = pd.DataFrame(cars)

            with st.expander("🔍 Filterindstillinger", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_filter = st.multiselect(
                        "Status",
                        options=["available", "rented", "maintenance"],
                        default=["available", "rented", "maintenance"],
                    )
                with col2:
                    if "brand" in df.columns:
                        brands = ["Alle"] + sorted(df["brand"].unique().tolist())
                        brand_filter = st.selectbox("Mærke", brands)
                    else:
                        brand_filter = None
                with col3:
                    if "fuel_type" in df.columns:
                        fuel_types = ["Alle"] + sorted(df["fuel_type"].unique().tolist())
                        fuel_filter = st.selectbox("Brændstoftype", fuel_types)
                    else:
                        fuel_filter = None

            if status_filter and "status" in df.columns:
                df = df[df["status"].isin(status_filter)]
            if brand_filter and brand_filter != "Alle" and "brand" in df.columns:
                df = df[df["brand"] == brand_filter]
            if fuel_filter and fuel_filter != "Alle" and "fuel_type" in df.columns:
                df = df[df["fuel_type"] == fuel_filter]

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Viser <strong>{len(df)}</strong> køretøjer</p>",
                unsafe_allow_html=True,
            )
            st.dataframe(df, use_container_width=True, hide_index=True, height=500)
        else:
            st.info(
                "Ingen køretøjer registreret i flåden endnu. Tilføj det første køretøj for at komme i gang."
            )

    with tab2:
        with st.form("add_car_form", clear_on_submit=True):
            st.markdown("### 🚘 Køretøjsoplysninger")

            col1, col2, col3 = st.columns(3)
            with col1:
                brand = st.text_input("Mærke *", placeholder="Toyota, BMW, Tesla...")
                model = st.text_input("Model *", placeholder="Camry, X5, Model 3...")
                year = st.number_input(
                    "Årgang *", min_value=1990, max_value=2030, value=2024
                )
            with col2:
                license_plate = st.text_input("Nummerplade *", placeholder="AB12345")
                km_driven = st.number_input(
                    "Kilometer kørt *", min_value=0, value=0, step=1000
                )
                fuel_type = st.selectbox(
                    "Brændstoftype *",
                    ["Benzin", "Diesel", "Elektrisk", "Hybrid", "Plug-in Hybrid"],
                )
            with col3:
                status = st.selectbox(
                    "Status *", ["available", "rented", "maintenance"]
                )
                purchase_price = st.number_input(
                    "Indkøbspris (DKK) *", min_value=0, value=0, step=10000
                )
                location = st.text_input(
                    "Placering *", placeholder="København, Aarhus..."
                )

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                submitted = st.form_submit_button(
                    "🚀 Tilføj køretøj til flåden", use_container_width=True
                )

            if submitted:
                if not all([brand, model, license_plate, location]):
                    st.error("Udfyld venligst alle felter markeret med *.")
                else:
                    new_car = {
                        "brand": brand,
                        "model": model,
                        "year": int(year),
                        "license_plate": license_plate,
                        "km_driven": int(km_driven),
                        "fuel_type": fuel_type,
                        "status": status,
                        "purchase_price": int(purchase_price),
                        "location": location,
                    }
                    _, error = api_post("/cars", new_car)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"{brand} {model} er tilføjet til flåden.")
                        st.balloons()

def customers_page():
    render_page_header(
        "👥 Kundehåndtering",
        "Overblik over og oprettelse af kunder i systemet.",
    )

    tab1, tab2 = st.tabs(["📋 Alle kunder", "➕ Ny kunde"])

    with tab1:
        customers, error = api_get("/customers")
        if error:
            st.error(f"❌ {error}")
        elif customers:
            df = pd.DataFrame(customers)

            search = st.text_input(
                "🔍 Søg i kunder",
                placeholder="Søg efter navn, e-mail eller CPR-nummer...",
            )
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

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Viser <strong>{len(df)}</strong> kunder</p>",
                unsafe_allow_html=True,
            )
            st.dataframe(df, use_container_width=True, hide_index=True, height=500)
        else:
            st.info("Der er endnu ingen kunder registreret. Opret den første kunde for at komme i gang.")

    with tab2:
        with st.form("add_customer_form", clear_on_submit=True):
            st.markdown("### 👤 Personoplysninger")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Fornavn *", placeholder="Anna")
                last_name = st.text_input("Efternavn *", placeholder="Jensen")
                email = st.text_input("E-mail *", placeholder="anna.jensen@example.com")
                cpr_number = st.text_input(
                    "CPR-nummer *", placeholder="DDMMÅÅ-XXXX"
                )
            with col2:
                address = st.text_input(
                    "Adresse *", placeholder="Vestergade 10, 2. th."
                )
                postal_code = st.text_input("Postnummer *", placeholder="1000")
                city = st.text_input("By *", placeholder="København")

            st.markdown("### 💳 Bankoplysninger (valgfrit)")
            col3, col4 = st.columns(2)
            with col3:
                registration_number = st.text_input(
                    "Registreringsnummer", placeholder="1234"
                )
                account_number = st.text_input(
                    "Kontonummer", placeholder="1234567890"
                )
            with col4:
                comments = st.text_area(
                    "Noter",
                    placeholder="Evt. supplerende oplysninger om kunden...",
                    height=100,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                submitted = st.form_submit_button(
                    "✨ Opret kundeprofil", use_container_width=True
                )

            if submitted:
                if not all(
                    [name, last_name, email, cpr_number, address, postal_code, city]
                ):
                    st.error("Udfyld venligst alle felter markeret med *.")
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
                        st.success(f"Kundeprofil for {name} {last_name} er oprettet.")
                        st.balloons()

def contracts_page():
    render_page_header(
        "📄 Kontrakthåndtering",
        "Opret og få overblik over abonnements-kontrakter.",
    )

    tab1, tab2 = st.tabs(["📋 Alle kontrakter", "➕ Ny kontrakt"])

    with tab1:
        contracts, error = api_get("/contracts")
        if error:
            st.error(f"❌ {error}")
        elif contracts:
            df = pd.DataFrame(contracts)
            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Viser <strong>{len(df)}</strong> kontrakter</p>",
                unsafe_allow_html=True,
            )
            st.dataframe(df, use_container_width=True, hide_index=True, height=500)
        else:
            st.info("Der er endnu ingen kontrakter oprettet. Opret den første kontrakt for at komme i gang.")

    with tab2:
        with st.form("contract_form", clear_on_submit=True):
            st.markdown("### 👤 Kundeoplysninger")
            st.markdown(
                "<p style='color: #64748b; font-size: 0.9rem;'>Angiv e-mail på eksisterende kunde, eller udfyld alle felter for at oprette en ny kunde i forbindelse med kontrakten.</p>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input(
                    "Kundens e-mail *", placeholder="kunde@example.com"
                )
                name = st.text_input(
                    "Fornavn (ny kunde)", placeholder="Tom, hvis kunden allerede findes"
                )
                last_name = st.text_input("Efternavn (ny kunde)")
                cpr_number = st.text_input("CPR-nummer (ny kunde)")
            with col2:
                address = st.text_input("Adresse (ny kunde)")
                postal_code = st.text_input("Postnummer (ny kunde)")
                city = st.text_input("By (ny kunde)")

            col3, col4 = st.columns(2)
            with col3:
                registration_number = st.text_input(
                    "Registreringsnummer (ny kunde)"
                )
            with col4:
                account_number = st.text_input(
                    "Kontonummer (ny kunde)"
                )

            comments = st.text_area(
                "Noter til kontrakten", placeholder="Evt. supplerende aftalevilkår..."
            )

            st.markdown("### 🚗 Køretøj til kontrakten")
            col5, col6 = st.columns(2)
            with col5:
                brand = st.text_input(
                    "Bil-mærke *", placeholder="Toyota, BMW, Tesla..."
                )
                model = st.text_input(
                    "Bil-model *", placeholder="Camry, X5, Model 3..."
                )
            with col6:
                year = st.number_input(
                    "Årgang *", min_value=1990, max_value=2030, value=2024
                )
                fuel_type = st.selectbox(
                    "Brændstoftype *",
                    ["Benzin", "Diesel", "Elektrisk", "Hybrid", "Plug-in Hybrid"],
                )

            st.markdown("### 💰 Økonomi og periode")
            col7, col8 = st.columns(2)
            with col7:
                start_date = st.date_input("Startdato *", value=datetime.now())
                sub_price_per_month = st.number_input(
                    "Månedlig abonnementspris (DKK) *",
                    min_value=0,
                    value=0,
                    step=100,
                )
            with col8:
                end_date = st.date_input("Slutdato *", value=datetime.now())

            if start_date and end_date:
                duration = (end_date - start_date).days
                st.markdown(
                    f"<p style='color: #0ea5e9; font-weight: 600; margin-top: 0.5rem;'>Kontraktlængde: {duration} dage (~{duration // 30} måneder)</p>",
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])
            with col_btn:
                submitted = st.form_submit_button(
                    "📝 Opret kontrakt", use_container_width=True
                )

            if submitted:
                if not all([email, brand, model, fuel_type]):
                    st.error("Udfyld som minimum e-mail, bil-mærke, model og brændstoftype.")
                elif start_date >= end_date:
                    st.error("Slutdato skal ligge efter startdato.")
                else:
                    payload = {
                        "email": email,
                        "name": name,
                        "last_name": last_name,
                        "address": address,
                        "postal_code": postal_code,
                        "city": city,
                        "cpr_number": cpr_number,
                        "registration_number": registration_number,
                        "account_number": account_number,
                        "comments": comments,
                        "brand": brand,
                        "model": model, 
                        "year": int(year),
                        "fuel_type": fuel_type,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "sub_price_per_month": int(sub_price_per_month),
                    }
                    _, error = api_post("/contracts", payload)
                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"Kontrakten for {brand} {model} er oprettet.")
                        st.balloons()

# Routing
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
elif st.session_state.page == "AI Damage":
    ai_damage_page()

render_footer()
