import streamlit as st
import textwrap

# Helper function to clean up HTML strings
def _html(s: str) -> str:
    """Helper function to clean up HTML strings"""
    return textwrap.dedent(s).strip()

# UI Components
def display_metric_card(title: str, value, icon: str):
    """Renders a metric card with title, value, and icon"""
    st.markdown(
        _html(f"""
        <div class="metric-card">
            <div class="metric-title">{icon} {title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

# Renders a status badge
def display_status_badge(label: str, value, color: str = "#0ea5e9"):
    """Renders a status badge with label and value"""
    st.markdown(
        _html(f"""
        <div class="status-card">
            <p style="margin: 0; color: #475569; font-size: 0.85rem; font-weight: 600;
                      text-transform: uppercase; letter-spacing: 0.05em;">
                {label}
            </p>
            <p style="margin: 0.5rem 0 0 0; color: {color}; font-size: 2rem;
                      font-weight: 800; line-height: 1;">
                {value}
            </p>
        </div>
        """),
        unsafe_allow_html=True,
    )

# Renders the page header
def render_page_header(title: str, subtitle: str):
    """Renders the page header with title and subtitle"""
    st.markdown(
        _html(f"""
        <h1 style="color:#0f172a; font-weight:800; font-size:2rem; margin:0;">{title}</h1>
        <p class="header-subtitle">{subtitle}</p>
        """),
        unsafe_allow_html=True,
    )

# Helper to create a navigation button
def _create_nav_button(col, label: str, page: str, current_page: str, key: str = None, help_text: str = None, button_type: str = None):
    """Helper to create a navigation button"""
    with col:
        # Determine button type - allow override or auto-detect
        if button_type is None:
            button_type = "primary" if current_page == page else "secondary"
        
        if st.button(
            label,
            use_container_width=True,
            type=button_type,
            help=help_text,
            key=key,
        ):
            st.session_state.page = page
            st.rerun()

# Renders the header with navigation buttons
def render_header(current_page: str):
    """Renders the header with navigation buttons"""
    has_jwt = bool(st.session_state.get("jwt"))

    col_logo, col_home, col_spacer, col_nav1, col_nav2, col_nav3, col_nav4, col_logout = st.columns(
        [2.1, 0.5, 3.0, 1.2, 1.2, 1.2, 1.2, 0.5]
    )

    with col_logo:
        try:
            st.image("components/Bilabonnement.svg", width=350)
        except Exception:
            st.markdown(
                _html("""
                <div style="display:flex; align-items:center; gap:0.5rem;">
                    <div style="font-size:2rem;">🚗</div>
                    <div>
                        <h2 style="margin:0; color:#0ea5e9; font-size:1.4rem;">BILABONNEMENT</h2>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

    if not has_jwt:
        st.markdown(
            _html("<hr style='margin:0.5rem 0 1.5rem 0; border:none; border-top:1px solid #e2e8f0;'>"),
            unsafe_allow_html=True,
        )
        return

    # Navigation buttons
    _create_nav_button(col_home, "🏠", "Dashboard", current_page, "home_btn", "Dashboard")
    _create_nav_button(col_nav1, "🚗 Cars", "Cars", current_page)
    _create_nav_button(col_nav2, "👥 Customers", "Customers", current_page)
    _create_nav_button(col_nav3, "📄 Contracts", "Contracts", current_page)
    _create_nav_button(col_nav4, "🧠 AI Damage", "AI Damage", current_page)

    # Logout button
    with col_logout:
        if st.button(
            "🚪",
            use_container_width=True,
            type="primary",
            help="Logout",
            key="logout_btn_header",
        ):
            st.session_state.clear()
            st.session_state.page = "Login"
            st.rerun()

    st.markdown(
        _html("<hr style='margin:0.5rem 0 1.5rem 0; border:none; border-top:1px solid #e2e8f0;'>"),
        unsafe_allow_html=True,
    )

# Renders the footer with user info and status
def render_footer():
    """Renders the footer with user info and status"""
    role = st.session_state.get("role")
    username = st.session_state.get("username")
    has_jwt = bool(st.session_state.get("jwt"))

    right_side = ""
    if has_jwt:
        role_txt = role.capitalize() if role else "Unknown"
        user_txt = username if username else "Unknown"

        right_side = _html(f"""
        <span style="margin-right:1rem;">
            User: <span style="font-weight:700; color:#0f172a;">{user_txt}</span>
        </span>
        <span style="margin-right:1rem;">
            Role: <span style="font-weight:700; color:#0f172a;">{role_txt}</span>
        </span>
        """)

    footer_html = _html(f"""
    <div class="footer-info">
        <div>
            <span style="font-weight:600; color:#1e293b;">Bilabonnement Dashboard</span>
            <span style="margin-left:1rem;">Version 1.0.0</span>
        </div>
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <span style="margin-right:1.5rem;">
                Status: <span style="color:#10b981;">● Online</span>
            </span>
            <span>
                Gateway: <span style="color:#10b981;">Active</span>
            </span>
            {right_side}
        </div>
    </div>
    """)

    st.markdown(footer_html, unsafe_allow_html=True)