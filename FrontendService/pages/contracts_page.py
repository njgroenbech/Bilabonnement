import streamlit as st
import pandas as pd
import time
from datetime import datetime
from api.api_client import api_get, api_post, api_delete
from components.ui_components import render_page_header

# Contract Management Page
def contracts_page():
    render_page_header("📄 Contract Management", "Create and manage subscription contracts")

    tab1, tab2 = st.tabs(["📋 All Contracts", "➕ New Contract"])

    # TAB 1: All Contracts
    with tab1:
        contracts, error = api_get("/contracts")

        if error:
            st.error(f"❌ {error}")
        elif contracts:
            df = pd.DataFrame(contracts)

            st.markdown(
                f"<p style='color: #64748b; margin: 1rem 0;'>Showing <strong>{len(df)}</strong> contracts</p>",
                unsafe_allow_html=True,
            )

            # Display table
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                height=400,
                disabled=df.columns.tolist(),
                num_rows="fixed",
                key="contract_table"
            )

            # Delete section
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col2:
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
                                st.success("✅ Contract deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()
        else:
            st.info("ℹ️ No contracts found. Create your first contract to get started!")

    # TAB 2: New Contract
    with tab2:
        st.markdown("### 📝 Create New Contract")

        # Load customers
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
            active_customer_ids = [c['customer_id'] for c in contracts if c.get('status') == 'active']
        
        available_customers = [c for c in customers if c['customer_id'] not in active_customer_ids]

        if not available_customers:
            st.warning("⚠ No available customers. All customers already have active contracts.")
            st.info("💡 Tip: Delete an existing contract or add a new customer to create a contract.")
            return

        customer_options = {f"{c['name']} {c['last_name']} ({c['email']})": c for c in available_customers}

        selected_customer = st.selectbox("👤 Select Customer *", list(customer_options.keys()))
        customer = customer_options[selected_customer]

        # Load cars
        cars, car_error = api_get("/cars")
        if car_error:
            st.error("❌ Failed to load cars")
            return

        available_cars = [c for c in cars if c.get("status") == "available"]

        if not available_cars:
            st.warning("⚠ No available cars. All cars are rented or under maintenance.")
            return

        car_options = {f"{c['brand']} {c['model']} – {c['license_plate']}": c for c in available_cars}

        selected_car = st.selectbox("🚗 Select Available Car *", list(car_options.keys()))
        car = car_options[selected_car]

        # Contract period
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

        # Subscription price
        st.markdown("### 💰 Subscription Details")

        sub_price_per_month = car.get('sub_price_per_month', 0)

        st.markdown(
            f"<p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>"
            f"Subscription price per month: <strong style='color: #0ea5e9;'>{sub_price_per_month:,} DKK</strong>"
            f"</p>",
            unsafe_allow_html=True
        )

        st.info(f"💡 This is the standard price for the {car['brand']} {car['model']}")

        # Submit button
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
                "sub_price_per_month": int(sub_price_per_month),
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