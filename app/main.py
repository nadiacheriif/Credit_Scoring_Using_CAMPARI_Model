from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scoring import score_client

app = FastAPI(title="Credit Scoring API")


class ClientInput(BaseModel):
    account_status: str
    duration: float
    credit_history: str
    purpose: str
    credit_amount: float
    savings: str
    employment: str
    installment_rate: int
    personal_status: str
    guarantors: str
    residence: int
    property: str
    age: int
    other_installments: str
    housing: str
    credit_cards: int
    job: str
    dependents: int
    phone: str
    foreign_worker: str


@app.get("/")
def health():
    return {"status": "API running"}


@app.post("/score")
def score(data: ClientInput):
    try:
        return score_client(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
