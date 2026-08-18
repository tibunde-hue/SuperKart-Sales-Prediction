import streamlit as st
import requests
import pandas as pd

st.title("SuperKart Sales Prediction App")

backend_url_online = "http://backend:7860/v1/predict"
backend_url_batch = "http://backend:7860/v1/predictbatch"

st.header("Online Inference")
weight = st.number_input("Product Weight", value=12.66)
sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
area = st.number_input("Product Allocated Area", value=0.027)
mrp = st.number_input("Product MRP", value=117.08)
size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"])
pid_char = st.selectbox("Product Id Char (e.g., FD)", ["FD", "NC", "DR"])
age = st.number_input("Store Age Years", value=16)
cat = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

if st.button("Predict"):
    payload = {
        "Product_Weight": weight, "Product_Sugar_Content": sugar,
        "Product_Allocated_Area": area, "Product_MRP": mrp,
        "Store_Size": size, "Store_Location_City_Type": city,
        "Store_Type": store_type, "Product_Id_char": pid_char,
        "Store_Age_Years": age, "Product_Type_Category": cat
    }
    response = requests.post(backend_url_online, json=payload)
    if response.status_code == 200:
        st.success(f"Predicted Sales: {response.json()['prediction']:.2f}")
    else:
        st.error("Error connecting to backend.")

st.header("Batch Inference")
uploaded_file = st.file_uploader("Upload CSV file", type="csv")
if uploaded_file is not None and st.button("Predict Batch"):
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(backend_url_batch, files=files)
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Error connecting to backend.")
