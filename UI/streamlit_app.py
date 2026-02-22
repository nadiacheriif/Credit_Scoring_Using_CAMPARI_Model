import streamlit as st
from app.scoring import score_client

st.set_page_config(page_title="Credit Scoring App", layout="centered")

st.title("💳 Credit Scoring Application")

st.markdown("Fill in client information to generate credit decision.")

# ---------------------------------------------------
# INPUT FIELDS (MUST MATCH TRAINING DATA EXACTLY)
# ---------------------------------------------------

account_status = st.selectbox(
    "Account Status",
    ["A11", "A12", "A13", "A14"]
)

duration = st.number_input("Duration (months)", min_value=1)

credit_history = st.selectbox(
    "Credit History",
    ["A30", "A31", "A32", "A33", "A34"]
)

purpose = st.selectbox(
    "Purpose",
    ["A40", "A41", "A42", "A43", "A44", "A45", "A46"]
)

credit_amount = st.number_input("Credit Amount", min_value=0)

savings = st.selectbox(
    "Savings",
    ["A61", "A62", "A63", "A64", "A65"]
)

employment = st.selectbox(
    "Employment Duration",
    ["A71", "A72", "A73", "A74", "A75"]
)

installment_rate = st.selectbox(
    "Installment Rate",
    [1, 2, 3, 4]
)

personal_status = st.selectbox(
    "Personal Status",
    ["A91", "A92", "A93", "A94"]
)

guarantors = st.selectbox(
    "Guarantors",
    ["A101", "A102", "A103"]
)

# ✅ VERY IMPORTANT — This was missing before
residence = st.selectbox(
    "Residence Since (years)",
    [1, 2, 3, 4]
)

property_value = st.selectbox(
    "Property",
    ["A121", "A122", "A123", "A124"]
)

age = st.number_input("Age", min_value=18)

other_installments = st.selectbox(
    "Other Installments",
    ["A141", "A142", "A143"]
)

housing = st.selectbox(
    "Housing",
    ["A151", "A152", "A153"]
)

credit_cards = st.selectbox(
    "Number of Existing Credits",
    [1, 2, 3, 4]
)

job = st.selectbox(
    "Job",
    ["A171", "A172", "A173", "A174"]
)

dependents = st.selectbox(
    "Dependents",
    [1, 2]
)

phone = st.selectbox(
    "Phone",
    ["A191", "A192"]
)

foreign_worker = st.selectbox(
    "Foreign Worker",
    ["A201", "A202"]
)

# ---------------------------------------------------
# SCORING BUTTON
# ---------------------------------------------------

if st.button("🔎 Score Client"):

    # 🔥 Clean explicit payload (NO locals())
    input_data = {
        "account_status": account_status,
        "duration": duration,
        "credit_history": credit_history,
        "purpose": purpose,
        "credit_amount": credit_amount,
        "savings": savings,
        "employment": employment,
        "installment_rate": installment_rate,
        "personal_status": personal_status,
        "guarantors": guarantors,
        "residence": residence,
        "property": property_value,
        "age": age,
        "other_installments": other_installments,
        "housing": housing,
        "credit_cards": credit_cards,
        "job": job,
        "dependents": dependents,
        "phone": phone,
        "foreign_worker": foreign_worker,
    }

    try:
        result = score_client(input_data)

        st.success("Scoring Completed")

        st.subheader("📊 Results")
        st.write(f"**Probability of Default:** {result['probability_default']}")
        st.write(f"**Credit Score:** {result['credit_score']}")
        st.write(f"**Decision:** {result['decision']}")

    except Exception as e:
        st.error(f"Error during scoring: {e}")
