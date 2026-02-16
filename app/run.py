from app.scoring import score_client

sample_input = {
    "duration": 12,
    "credit_amount": 3000,
    "installment_rate": 2,
    "age": 35,
    "credit_cards": 1,
    "dependents": 1,
    "account_status": "A11",
    "credit_history": "A32",
    "purpose": "A40",
    "savings": "A61",
    "employment": "A73",
    "personal_status": "A93",
    "guarantors": "A101",
    "property": "A121",
    "other_installments": "A141",
    "housing": "A151",
    "job": "A173",
    "phone": "A192",
    "foreign_worker": "A201",
}

result = score_client(sample_input)

print(result)
