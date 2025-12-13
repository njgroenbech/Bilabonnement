import streamlit as st
import textwrap


def _html(s: str) -> str:
    """
    Make HTML safe for Streamlit markdown:
    - remove indentation (dedent)
    - remove leading/trailing newlines/spaces (strip)
    This prevents Markdown from interpreting indented lines as code blocks.
    """
    return textwrap.dedent(s).strip()


def display_metric_card(title: str, value, icon: str):
    st.markdown(
        _html(f"""
        <div class="metric-card">
            <div class="metric-title">{icon} {title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def display_status_badge(label: str, value, color: str = "#0ea5e9"):
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


def render_page_header(title: str, subtitle: str):
    st.markdown(
        _html(f"""
        <h1 style="color:#0f172a; font-weight:800; font-size:2rem; margin:0;">{title}</h1>
        <p class="header-subtitle">{subtitle}</p>
        """),
        unsafe_allow_html=True,
    )


def render_header(current_page: str):
    has_jwt = bool(st.session_state.get("jwt"))

    col_logo, col_home, col_spacer, col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(
        [2.1, 0.5, 3.3, 1.2, 1.2, 1.2, 1.4]
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

    # Not logged in => only show separator line (no nav buttons)
    if not has_jwt:
        st.markdown(
            _html("<hr style='margin:0.5rem 0 1.5rem 0; border:none; border-top:1px solid #e2e8f0;'>"),
            unsafe_allow_html=True,
        )
        return

    # Logged in => show nav buttons
    with col_home:
        if st.button(
            "🏠",
            use_container_width=True,
            type="primary" if current_page == "Dashboard" else "secondary",
            help="Dashboard",
            key="home_btn",
        ):
            st.session_state.page = "Dashboard"
            st.rerun()

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

    with col_nav4:
        if st.button(
            "🧠 AI Damage",
            use_container_width=True,
            type="primary" if current_page == "AI Damage" else "secondary",
        ):
            st.session_state.page = "AI Damage"
            st.rerun()

    st.markdown(
        _html("<hr style='margin:0.5rem 0 1.5rem 0; border:none; border-top:1px solid #e2e8f0;'>"),
        unsafe_allow_html=True,
    )


def render_footer():
    role = st.session_state.get("role")
    username = st.session_state.get("username")
    has_jwt = bool(st.session_state.get("jwt"))

    right_side = ""
    if has_jwt:
        role_txt = (role.capitalize() if role else "Unknown")
        user_txt = (username if username else "Unknown")

        # IMPORTANT: no leading indentation in final string (handled by _html)
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

    if has_jwt:
        col_spacer, col_btn = st.columns([8, 2])
        with col_btn:
            if st.button("Logout", key="logout_btn", use_container_width=True):
                st.session_state.clear()
                st.session_state.page = "Login"
                st.rerun()
