def validate_input(df):

    if not (df['duration'] > 0).all():
        raise ValueError("Invalid loan duration")

    if not (df['credit_amount'] > 0).all():
        raise ValueError("Invalid credit amount")

    if not df['installment_rate'].between(1, 4).all():
        raise ValueError("Invalid installment rate")

    if not (df['age'] >= 18).all():
        raise ValueError("Underage applicant")

    if not (df['credit_cards'] >= 0).all():
        raise ValueError("Invalid credit cards number")

    if not (df['dependents'] >= 0).all():
        raise ValueError("Invalid dependents number")

    expected_categories = {
        "account_status": {"A11","A12","A13","A14"},
        "credit_history": {"A30","A31","A32","A33","A34"},
        "purpose": {"A40","A41","A42","A43","A44","A45","A46","A48","A49","A410"},
        "savings": {"A61","A62","A63","A64","A65"},
        "employment": {"A71","A72","A73","A74","A75"},
        "personal_status": {"A91","A92","A93","A94","A95"},
        "guarantors": {"A101","A102","A103"},
        "property": {"A121","A122","A123","A124"},
        "other_installments": {"A141","A142","A143"},
        "housing": {"A151","A152","A153"},
        "job": {"A171","A172","A173","A174"},
        "phone": {"A191","A192"},
        "foreign_worker": {"A201","A202"},
    }

    for col, allowed in expected_categories.items():
        invalid = set(df[col].unique()) - allowed
        if len(invalid) > 0:
            raise ValueError(f"Invalid category in {col}: {invalid}")

    return True



##this should be called in the API endpoint before making predictions to ensure the input data is valid.