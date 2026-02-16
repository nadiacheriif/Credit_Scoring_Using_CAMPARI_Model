from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scoring import score_client

app = FastAPI(title="CAMPARI Credit Scoring API")

class ClientInput(BaseModel):
    duration: float
    credit_amount: float
    installment_rate: int
    age: int
    credit_cards: int
    dependents: int
    account_status: str
    credit_history: str
    purpose: str
    savings: str
    employment: str
    personal_status: str
    guarantors: str
    property: str
    other_installments: str
    housing: str
    job: str
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
