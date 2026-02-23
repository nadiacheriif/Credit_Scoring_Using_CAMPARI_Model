import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from app.scoring import score_client

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="CAMPARI Credit Scoring",
    layout="wide"
)

# ===============================
# DARK MODE TOGGLE
# ===============================

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: white; }
        section[data-testid="stSidebar"] { background-color: #161b22; }
        label, p, span, div { color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# ===============================
# BRANDING
# ===============================

st.markdown("""
<h1 style='text-align: center; color:#1f4e79;'>
🏦 CAMPARI BANK - Credit Risk Decision System
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ===============================
# USER-FRIENDLY MAPPINGS
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

personal_status_map = {
    "Male - Single": "A93",
    "Male - Married/Widowed": "A94",
    "Male - Divorced": "A91",
    "Female - Married/Divorced": "A92"
}

other_installments_map = {
    "Bank": "A141",
    "Stores": "A142",
    "None": "A143"
}

# ===============================
# INPUT FORM
# ===============================

with st.form("credit_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        account_status = st.selectbox("Checking Account Status", list(account_status_map.keys()))
        duration = st.number_input("Loan Duration (months)", min_value=4, max_value=72)
        credit_history = st.selectbox("Credit History", list(credit_history_map.keys()))
        purpose = st.selectbox("Loan Purpose", list(purpose_map.keys()))

    with col2:
        credit_amount = st.number_input("Credit Amount (DM)", min_value=100)
        savings = st.selectbox("Savings Level", list(savings_map.keys()))
        employment = st.selectbox("Employment Duration", list(employment_map.keys()))
        installment_rate = st.slider("Installment Rate (%)", 1, 4)

    with col3:
        age = st.number_input("Age", min_value=18, max_value=75)
        housing = st.selectbox("Housing Type", list(housing_map.keys()))
        guarantors = st.selectbox("Guarantors", list(guarantors_map.keys()))
        property_value = st.selectbox("Property Type", list(property_map.keys()))

    col4, col5 = st.columns(2)

    with col4:
        residence = st.slider("Residence Duration (years)", 1, 4)
        personal_status = st.selectbox("Personal Status", list(personal_status_map.keys()))

    with col5:
        other_installments = st.selectbox("Other Installment Plans", list(other_installments_map.keys()))
        credit_cards = st.slider("Number of Existing Credits", 1, 4)

    submit = st.form_submit_button("🔎 Score Client")

# ===============================
# SCORING
# ===============================

if submit:

    with st.spinner("🔍 Analyzing client profile..."):
        time.sleep(1.2)

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
            "residence": residence,
            "personal_status": personal_status_map[personal_status],
            "other_installments": other_installments_map[other_installments],
            "credit_cards": credit_cards,
        }

        result = score_client(input_data)

    # ===============================
    # VALIDATION ERRORS
    # ===============================

    if "errors" in result:
        for error in result["errors"]:
            st.error(error)
        st.stop()

    score = result["credit_score"]
    probability = result["probability_default"]
    decision = result["decision"]

    # ===============================
    # ADAPTIVE GAUGE
    # ===============================

    bg_color = "#0e1117" if dark_mode else "white"
    font_color = "white" if dark_mode else "black"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Credit Score", 'font': {'color': font_color}},
        number={'font': {'color': font_color}},
        gauge={
            'axis': {'range': [300, 900], 'tickcolor': font_color},
            'bar': {'color': "#1f77b4"},
            'bgcolor': bg_color,
            'borderwidth': 2,
            'bordercolor': font_color,
            'steps': [
                {'range': [300, 500], 'color': "#ff4d4d"},
                {'range': [500, 650], 'color': "#ffa500"},
                {'range': [650, 900], 'color': "#4CAF50"},
            ],
        }
    ))

    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font={'color': font_color}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric("Probability of Default", round(probability, 3))

    if decision == "APPROVE":
        st.success("✅ LOAN APPROVED")
    elif decision == "REJECT":
        st.error("❌ LOAN REJECTED")
    else:
        st.warning("⚠️ MANUAL REVIEW REQUIRED")

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
    # IN-MEMORY PDF REPORT
    # ===============================

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("CAMPARI BANK - Credit Decision Report", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"Credit Score: {score}", styles["Normal"]))
    elements.append(Paragraph(f"Probability of Default: {round(probability,3)}", styles["Normal"]))
    elements.append(Paragraph(f"Decision: {decision}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    st.download_button(
        "📄 Download Decision Report",
        buffer,
        file_name="Credit_Decision_Report.pdf",
        mime="application/pdf"
    )
    