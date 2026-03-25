import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Customer Churn Predictor")

# Input
tenure = st.slider("Tenure", 0, 72, 12)
monthly = st.number_input("Monthly Charges", 0.0, 500.0, 50.0)
total = st.number_input("Total Charges", 0.0, 10000.0, 500.0)

contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment = st.selectbox("Payment", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
internet = st.selectbox("Internet", ["DSL", "Fiber optic", "No"])

if st.button("Predict"):

   payload = {
    "tenure": tenure,
    "monthly_charges": monthly_charges,
    "total_charges": total_charges,
    "Contract": contract,
    "PaymentMethod": payment_method,
    "InternetService": internet_service
}

    try:
        res = requests.post(f"{API_URL}/predict", json=payload)

        if res.status_code == 200:
            result = res.json()
            st.success(result)
        else:
            st.error(res.text)

    except:
        st.error("API not connected")