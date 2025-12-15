import requests
import streamlit as st
from components.ui_components import render_page_header
from api.api_client import api_get

DAMAGE_CHECK_URL = "http://gateway:5001/damagecheck"

def ai_damage_page():
    render_page_header(
        "🧠 AI Damage Check",
        "Upload one or more car images and get a simulated damage assessment.",
    )

    # fetch contracts
    contracts, _ = api_get("/contracts")
    cars, _ = api_get("/cars")

    # build car dict
    car_dict = {}
    if cars:
        for car in cars:
            car_dict[car["car_id"]] = f"{car['brand']} {car['model']}"

    # build contract options
    contract_options = {}
    for contract in contracts:
        if contract.get("status") == "active":
            car_name = car_dict.get(contract["car_id"], "Unknown Car")
            label = f"Contract #{contract['contract_id']} - {car_name}"
            contract_options[label] = contract
            
    selected_contract_key = st.selectbox("📄 Select Contract *", list(contract_options.keys()))
    selected_contract = contract_options[selected_contract_key]

    # display selected ids for report
    st.info(
        f"🚗 Car ID: {selected_contract['car_id']} | "
        f"👤 Customer ID: {selected_contract['customer_id']}"
    )

    uploaded_files = st.file_uploader(
        "Upload images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )

    if st.button("Run damage check", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one image.")
            return

        # add image file to payload
        files = [("images", (f.name, f.getvalue(), f.type)) for f in uploaded_files]

        # add contract and car id to payload
        data = {
            "contract_id": selected_contract["contract_id"],
            "car_id": selected_contract["car_id"]
        }

        try:
            resp = requests.post(DAMAGE_CHECK_URL, files=files, data=data, timeout=30)
        except Exception as e:
            st.error(f"Could not reach API Gateway: {e}")
            return

        if resp.status_code != 200:
            st.error(f"Backend error ({resp.status_code}): {resp.text}")
            return

        res = resp.json()
        status = res.get("overall_status")
        message = res.get("message", "")
        report_id = res.get("report_id")

        if status == "unclear":
            st.warning(f"🟡 {message}")
        elif status == "clear":
            st.success(f"🟢 {message}")
        elif status == "damage_found":
            st.error(f"🔴 {message}")
            level = res.get("damage_level")
            if level:
                st.info(f"Damage level: {level}")
        else:
            st.info("Unknown response:")
            st.json(res)

        if report_id:
            st.success(f"✅ Report saved with ID: {report_id}")
