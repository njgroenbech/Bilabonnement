
import os
import streamlit as st
import requests

# Allow overriding the gateway URL for local vs docker-compose runs
# Default uses the internal docker service name 'gateway'
DAMAGE_CHECK_URL = os.getenv(
    "DAMAGE_CHECK_URL",
    "http://gateway:5001/api/damage/check",
)


st.title("AI skadesvurdering")
st.write(
    "Upload billeder af bilen og tryk **Få vurdering** for at få en "
    "Vurdering af bilen"
)

uploaded_files = st.file_uploader(
    "Vælg et eller flere billeder",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
)

if st.button("Send til vurdering"):
    if not uploaded_files:
        st.warning("Upload mindst ét billede før du checker.")
    else:
        with st.spinner("Sender til AI-eftersyn"):
            files = [
                ("images", (f.name, f.getvalue(), f.type))
                for f in uploaded_files
            ]

            try:
                resp = requests.post(DAMAGE_CHECK_URL, files=files)
            except Exception as e:
                st.error(f"Kunne ikke kontakte API Gateway: {e}")
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
                        st.info(message or "Ukendt status.")

                  