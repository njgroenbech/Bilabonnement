import requests
import streamlit as st
from components.ui_components import render_page_header

DAMAGE_CHECK_URL = "http://gateway:5001/damagecheck"

def ai_damage_page():
    render_page_header(
        "🧠 AI Damage Check",
        "Upload one or more car images and get a simulated damage assessment.",
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

        files = [("images", (f.name, f.getvalue(), f.type)) for f in uploaded_files]

        try:
            resp = requests.post(DAMAGE_CHECK_URL, files=files, timeout=30)
        except Exception as e:
            st.error(f"Could not reach API Gateway: {e}")
            return

        if resp.status_code != 200:
            st.error(f"Backend error ({resp.status_code}): {resp.text}")
            return

        data = resp.json()
        status = data.get("overall_status")
        message = data.get("message", "")

        if status == "unclear":
            st.warning(f"🟡 {message}")
        elif status == "clear":
            st.success(f"🟢 {message}")
        elif status == "damage_found":
            st.error(f"🔴 {message}")
            level = data.get("damage_level")
            if level:
                st.info(f"Damage level: {level.get('label', level.get('key', 'unknown'))}")
        else:
            st.info("Unknown response:")
            st.json(data)
