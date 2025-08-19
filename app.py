import streamlit as st
import pandas as pd
from datetime import datetime
from Project import *

st.set_page_config(page_title="💊 Medicine Expiry and Stock Manager", layout="wide")

st.title("💊 Medicine Expiry and Stock Manager")

menu = ["Add Medicine", "Remove Medicine", "View Medicines", "Check Notifications"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Medicine":
    st.subheader("➕ Add New Medicine")
    name = st.text_input("Medicine Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    expiry_date = st.date_input("Expiry Date")

    if st.button("Add"):
        add_medicine(name, quantity, expiry_date.strftime("%Y-%m-%d"))
        st.success(f"✅ {name} added successfully!")

elif choice == "Remove Medicine":
    st.subheader("🗑️ Remove Medicine")
    df = load_data()
    if df.empty:
        st.warning("⚠️ No medicines found.")
    else:
        name_list = df["Name"].unique().tolist()
        name = st.selectbox("Select Medicine", name_list)
        if st.button("Remove"):
            remove_medicine(name)
            st.success(f"✅ {name} removed successfully!")

elif choice == "View Medicines":
    st.subheader("📋 Medicine Stock")
    df = load_data()
    if df.empty:
        st.warning("⚠️ No data available.")
    else:
        st.dataframe(df)

elif choice == "Check Notifications":
    st.subheader("🔔 Notifications")

    expired = check_expired()
    low_stock = check_low_stock()

    if expired.empty and low_stock.empty:
        st.success("✅ All medicines are safe and in stock.")
    else:
        if not expired.empty:
            st.error("⚠️ Expired Medicines:")
            st.dataframe(expired)

        if not low_stock.empty:
            st.warning("⚠️ Low Stock Medicines:")
            st.dataframe(low_stock)