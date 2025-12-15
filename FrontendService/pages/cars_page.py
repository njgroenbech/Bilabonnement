import streamlit as st
import pandas as pd
import time
from api.api_client import api_get, api_post, api_delete
from components.ui_components import render_page_header

# Car Fleet Management Page
def cars_page():
    render_page_header("🚗 Car Fleet Management", "Manage your complete vehicle inventory")

    tab1, tab2 = st.tabs(["📋 All Vehicles", "➕ Add New Vehicle"])

    # TAB 1: Vehicle List
    with tab1:
        cars, error = api_get("/cars")

        if error:
            st.error(f"❌ {error}")

        elif cars:
            df = pd.DataFrame(cars)

            # Filter Options
            with st.expander("🔍 Filter Options", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    status_filter = st.multiselect(
                        "Status",
                        options=["available", "rented", "maintenance"],
                        default=["available", "rented", "maintenance"],
                    )

                with col2:
                    brands = ["All"] + sorted(df["brand"].unique().tolist()) if "brand" in df.columns else ["All"]
                    brand_filter = st.selectbox("Brand", brands)

                with col3:
                    fuel_types = ["All"] + sorted(df["fuel_type"].unique().tolist()) if "fuel_type" in df.columns else ["All"]
                    fuel_filter = st.selectbox("Fuel Type", fuel_types)

            # Apply filters
            if status_filter and "status" in df.columns:
                df = df[df["status"].isin(status_filter)]

            if brand_filter != "All" and "brand" in df.columns:
                df = df[df["brand"] == brand_filter]

            if fuel_filter != "All" and "fuel_type" in df.columns:
                df = df[df["fuel_type"] == fuel_filter]

            # Column order
            preferred_order = [
                "brand",
                "model",
                "year",
                "license_plate",
                "car_id",
                "fuel_type",
                "km_driven",
                "location",
                "purchase_price",
                "sub_type",
                "sub_price_per_month",
                "status",
            ]

            df = df[[col for col in preferred_order if col in df.columns]]

            # Info text
            st.markdown(
                f"<p style='color:#64748b; margin:1rem 0;'>Showing <strong>{len(df)}</strong> vehicles</p>",
                unsafe_allow_html=True,
            )

            # Table
            st.data_editor(
                df,
                use_container_width=True,
                hide_index=True,
                height=400,
                disabled=df.columns.tolist(),
                num_rows="fixed",
                key="car_table"
            )

            # Delete vehicle
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])

            with col2:
                car_options = {
                    f"{c['brand']} {c['model']} ({c['license_plate']})": c["car_id"]
                    for c in cars
                }

                selected_to_delete = st.selectbox(
                    "Select vehicle to delete:",
                    options=[""] + list(car_options.keys()),
                    format_func=lambda x: "Select a vehicle..." if x == "" else x,
                )

                if selected_to_delete:
                    car_id = car_options[selected_to_delete]

                    if st.button("🗑️ Delete Selected Vehicle", type="primary", use_container_width=True):
                        with st.spinner("Deleting vehicle..."):
                            _, err = api_delete(f"/cars/{car_id}")
                            if err:
                                st.error(f"❌ Failed to delete: {err}")
                            else:
                                st.success("✅ Vehicle deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()

        else:
            st.info("ℹ️ No vehicles found in the fleet. Add your first vehicle to get started!")

    # TAB 2: Add New Vehicle
    with tab2:
        with st.form("add_car_form", clear_on_submit=True):
            st.markdown("### 🚘 Vehicle Details")

            col1, col2, col3 = st.columns(3)

            with col1:
                brand = st.text_input("Brand *")
                model = st.text_input("Model *")
                year = st.number_input("Year *", min_value=1990, max_value=2030, value=2024)

            with col2:
                license_plate = st.text_input("License Plate *")
                km_driven = st.number_input("Kilometers Driven *", min_value=0, step=1000)
                fuel_type = st.selectbox("Fuel Type *", ["gasoline", "diesel", "electric", "hybrid"])

            with col3:
                status = st.selectbox("Status *", ["available", "rented", "maintenance"])
                purchase_price = st.number_input("Purchase Price (DKK) *", min_value=0, step=10000)
                sub_type = st.selectbox("Subscription Type *", ["subscription", "mini-lease"])
                sub_price_per_month = st.number_input(
                    "Subscription price per month (DKK) *",
                    min_value=0,
                    step=500,
                )

            location = st.text_input("Location *")

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_btn, _ = st.columns([1, 1, 1])

            with col_btn:
                submitted = st.form_submit_button("🚀 Add Vehicle to Fleet", use_container_width=True)

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
                        "fuel_type": fuel_type,
                        "status": status,
                        "purchase_price": int(purchase_price),
                        "sub_type": sub_type,
                        "sub_price_per_month": int(sub_price_per_month),
                        "location": location,
                    }

                    _, error = api_post("/cars", new_car)

                    if error:
                        st.error(f"❌ {error}")
                    else:
                        st.success(f"✅ Successfully added {brand} {model} to the fleet!")
                        st.balloons()