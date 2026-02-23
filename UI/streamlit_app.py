import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from app.scoring import score_client

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(page_title="CAMPARI Credit Scoring", layout="wide")

# ===============================
# DARK MODE TOGGLE
# ===============================

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ===============================
# BANK BRANDING
# ===============================

st.markdown("""
<h1 style='text-align: center; color:#1f4e79;'>
🏦 CAMPARI BANK - Credit Risk Decision System
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ===============================
# USER FRIENDLY MAPPINGS
# ===============================

account_status_map = {
    "... < 0 DM": "A11",
    "0 <= Balance < 200 DM": "A12",
    "Balance >= 200 DM": "A13",
    "No checking account": "A14"
}

credit_history_map = {
    "All credits paid back": "A30",
    "All credits paid back at this bank": "A31",
    "Existing credits paid duly": "A32",
    "Delay in past payments": "A33",
    "Critical account": "A34"
}

purpose_map = {
    "Car (New)": "A40",
    "Car (Used)": "A41",
    "Furniture": "A42",
    "Education": "A46",
    "Business": "A49",
    "Other": "A410"
}

savings_map = {
    "< 100 DM": "A61",
    "100-500 DM": "A62",
    "500-1000 DM": "A63",
    ">= 1000 DM": "A64",
    "Unknown/None": "A65"
}

employment_map = {
    "Unemployed": "A71",
    "< 1 year": "A72",
    "1-4 years": "A73",
    "4-7 years": "A74",
    ">= 7 years": "A75"
}

housing_map = {
    "Rent": "A151",
    "Own": "A152",
    "For free": "A153"
}

guarantors_map = {
    "None": "A101",
    "Co-applicant": "A102",
    "Guarantor": "A103"
}

property_map = {
    "Real Estate": "A121",
    "Life Insurance": "A122",
    "Car / Other": "A123",
    "Unknown": "A124"
}

# ===============================
# INPUT FORM
# ===============================

with st.form("credit_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        account_status = st.selectbox("Checking Account Status", list(account_status_map.keys()))
        duration = st.number_input("Loan Duration (months)", min_value=1)
        credit_history = st.selectbox("Credit History", list(credit_history_map.keys()))
        purpose = st.selectbox("Loan Purpose", list(purpose_map.keys()))

    with col2:
        credit_amount = st.number_input("Credit Amount (DM)", min_value=0)
        savings = st.selectbox("Savings Level", list(savings_map.keys()))
        employment = st.selectbox("Employment Duration", list(employment_map.keys()))
        installment_rate = st.slider("Installment Rate (%)", 1, 4)

    with col3:
        age = st.number_input("Age", min_value=18)
        housing = st.selectbox("Housing Type", list(housing_map.keys()))
        guarantors = st.selectbox("Guarantors", list(guarantors_map.keys()))
        property_value = st.selectbox("Property Type", list(property_map.keys()))

    submit = st.form_submit_button("Score Client")

# ===============================
# SCORING
# ===============================

if submit:

    with st.spinner("🔍 Analyzing client profile..."):
        time.sleep(1.5)

        input_data = {
            "account_status": account_status_map[account_status],
            "duration": duration,
            "credit_history": credit_history_map[credit_history],
            "purpose": purpose_map[purpose],
            "credit_amount": credit_amount,
            "savings": savings_map[savings],
            "employment": employment_map[employment],
            "installment_rate": installment_rate,
            "age": age,
            "housing": housing_map[housing],
            "guarantors": guarantors_map[guarantors],
            "property": property_map[property_value],
            "residence": 2,
            "personal_status": "A93",
            "other_installments": "A143",
            "credit_cards": 1,
        }

        result = score_client(input_data)

    score = result["credit_score"]
    probability = result["probability_default"]
    decision = result["decision"]

    # ===============================
    # SCORE GAUGE
    # ===============================

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Credit Score"},
        gauge={
            'axis': {'range': [300, 900]},
            'steps': [
                {'range': [300, 500], 'color': "#ff4d4d"},
                {'range': [500, 650], 'color': "#ffa500"},
                {'range': [650, 900], 'color': "#4CAF50"},
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.metric("Probability of Default", round(probability, 3))

    st.success(f"Decision: {decision}")

    # ===============================
    # SCORE TREND SIMULATION
    # ===============================

    st.markdown("### 📈 Score Sensitivity Simulation")

    simulated_scores = [score - 30, score - 15, score, score + 15, score + 30]

    trend_df = pd.DataFrame({
        "Scenario": ["Worse", "Slightly Worse", "Current", "Slightly Better", "Better"],
        "Score": simulated_scores
    })

    st.line_chart(trend_df.set_index("Scenario"))

    # ===============================
    # PDF REPORT
    # ===============================

    def generate_pdf():
        doc = SimpleDocTemplate("decision_report.pdf", pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("CAMPARI BANK - Credit Decision Report", styles["Title"]))
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(f"Credit Score: {score}", styles["Normal"]))
        elements.append(Paragraph(f"Probability of Default: {round(probability,3)}", styles["Normal"]))
        elements.append(Paragraph(f"Decision: {decision}", styles["Normal"]))

        doc.build(elements)

    generate_pdf()

    with open("decision_report.pdf", "rb") as f:
        st.download_button(
            "📄 Download Decision Report",
            f,
            file_name="Credit_Decision_Report.pdf"
        )
