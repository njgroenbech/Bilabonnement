import streamlit as st
from pathlib import Path


def load_global_css():
    project_root = Path(__file__).resolve().parents[1]
    css_path = project_root / "global_styles.css"

    if not css_path.exists():
        st.error(f"Global CSS file not found: {css_path}")
        return

    with open(css_path, "r") as f:
        css = f.read()

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)