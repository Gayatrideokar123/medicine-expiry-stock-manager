import streamlit as st
import pandas as pd

st.title("Medicine Expiry & Stock Manager")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Home", "Add Medicine", "View Medicines"])

st.write(f"You are on page: {page}")
