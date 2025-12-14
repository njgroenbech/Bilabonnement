import streamlit as st
import pandas as pd
import time
from api.api_client import api_get, api_post, api_delete
from components.ui_components import render_page_header

# Customer Management Page
def customers_page():
    render_page_header("👥 Customer Management", "Manage your customer database")

    tab1, tab2 = st.tabs(["📋 All Customers", "➕ New Customer"])

    # TAB 1: Customer list
    with tab1:
        customers, error = api_get("/customers")
        contracts, _ = api_get("/contracts")

        if error:
            st.error(f"❌ {error}")

        elif customers:
            df = pd.DataFrame(customers)

            # Active contracts
            active_customer_ids = []
            if contracts:
                active_customer_ids = [
                    int(c["customer_id"])
                    for c in contracts
                    if c.get("status") == "active"
                ]

            df["has_active_contract"] = df["customer_id"].isin(active_customer_ids)

            # Search and filter
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
                    key="customer_filter",
                )

            if search:
                search_lower = search.lower()
                df = df[
                    df.apply(
                        lambda row: row.astype(str)
                        .str.lower()
                        .str.contains(search_lower)
                        .any(),
                        axis=1,
                    )
                ]

            if filter_option == "Active Contracts":
                df = df[df["has_active_contract"] == True]
            elif filter_option == "Available":
                df = df[df["has_active_contract"] == False]

            # Column order
            preferred_order = [
                "name",
                "last_name",
                "email",
                "cpr_number",
                "address",
                "postal_code",
                "city",
                "registration_number",
                "account_number",
                "comments",
                "has_active_contract",
                "customer_id",
            ]

            df = df[[col for col in preferred_order if col in df.columns]]

            st.markdown(
                f"<p style='color:#64748b; margin:1rem 0;'>Showing <strong>{len(df)}</strong> customers</p>",
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
                key="customer_table",
            )

            # Delete customer
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 2])

            with col2:
                customer_options = {
                    f"{c['name']} {c['last_name']} - {c['email']}": c["customer_id"]
                    for c in customers
                }

                selected_to_delete = st.selectbox(
                    "Select customer to delete:",
                    options=[""] + list(customer_options.keys()),
                    format_func=lambda x: "Select a customer..." if x == "" else x,
                    key="customer_delete_select",
                )

                if selected_to_delete:
                    customer_id = customer_options[selected_to_delete]

                    if st.button(
                        "🗑️ Delete Selected Customer",
                        type="primary",
                        use_container_width=True,
                        key="customer_delete_btn",
                    ):
                        with st.spinner("Deleting customer..."):
                            _, err = api_delete(f"/customers/{customer_id}")
                            if err:
                                st.error(f"❌ Failed to delete: {err}")
                            else:
                                st.success("✅ Customer deleted successfully!")
                                time.sleep(0.5)
                                st.rerun()

        else:
            st.info("ℹ️ No customers found. Add your first customer to get started!")

    # TAB 2: Add new customer
    with tab2:
        with st.form("add_customer_form", clear_on_submit=True):
            st.markdown("### 👤 Personal Information")

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("First Name *", placeholder="John")
                last_name = st.text_input("Last Name *", placeholder="Doe")
                email = st.text_input("Email *", placeholder="john.doe@example.com")
                cpr_number = st.text_input("CPR Number *", placeholder="DDMMYY-XXXX")

            with col2:
                address = st.text_input("Address *", placeholder="Vestergade 10, 2. th")
                postal_code = st.text_input("Postal Code *", placeholder="1000")
                city = st.text_input("City *", placeholder="Copenhagen")

            st.markdown("### 💳 Banking Information")
            col3, col4 = st.columns(2)

            with col3:
                registration_number = st.text_input("Registration Number", placeholder="1234")
                account_number = st.text_input("Account Number", placeholder="1234567890")

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