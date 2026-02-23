def validate_input(data):
    errors = []

    # =============================
    # Numeric sanity checks
    # =============================

    if data["age"] < 18 or data["age"] > 75:
        errors.append("Age must be between 18 and 75.")

    if data["credit_amount"] <= 0:
        errors.append("Credit amount must be positive.")

    if data["duration"] < 4 or data["duration"] > 72:
        errors.append("Loan duration must be between 4 and 72 months.")

    if data["installment_rate"] not in [1, 2, 3, 4]:
        errors.append("Installment rate must be between 1 and 4.")

    # =============================
    # Logical consistency checks
    # =============================

    if data["employment"] == "A71" and data["credit_amount"] > 20000:
        errors.append("Unemployed applicants cannot request very high loans.")

    if data["age"] < 21 and data["credit_amount"] > 15000:
        errors.append("Young applicants requesting large loans require review.")

    return errors