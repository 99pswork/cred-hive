# main.py

from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import List, Optional

app = FastAPI()

# 1. Company Name:
# 2. Address:
# 3. Registration Date:
# 4. Number of Employees:
# 5. Raised Capital:
# 6. Turnover:
# 7. Net Profit:
# 8. Contact Number:
# 9. Contact Email:
# 10. Company Website:
# 11. Loan Amount:
# 12. Loan Interest (%):
# 13. Account Status:
# Sample data model

class CreditInfo(BaseModel):
    id: int
    company_name: str
    address: str
    registration_date: date
    number_of_employees: int
    raisedCapital: int
    turnOver: int
    netProfit: int
    contactNumber: str
    contactEmail: EmailStr
    companyWebsite: HttpUrl
    loanAmount: int
    loanInterest: float
    accountStatus: str

# In-memory database (replace this with a database in a real-world scenario)
db = {
    1: CreditInfo(
        id=1,
        company_name="ABC Corporation",
        address="123 Main Street, Cityville",
        registration_date="2022-01-01",
        number_of_employees=100,
        raisedCapital=5000000,
        turnOver=2000000,
        netProfit=500000,
        contactNumber="+1 123-456-7890",
        contactEmail="info@abccorp.com",
        companyWebsite="https://www.abccorp.com",
        loanAmount=1000000,
        loanInterest=5.0,
        accountStatus="Active"
    ),

    2: CreditInfo(
        id=2,
        company_name="XYZ Ltd",
        address="456 Oak Avenue, Townsville",
        registration_date="2021-12-15",
        number_of_employees=50,
        raisedCapital=3000000,
        turnOver=1500000,
        netProfit=300000,
        contactNumber="+1 987-654-3210",
        contactEmail="info@xyzltd.com",
        companyWebsite="https://www.xyzltd.com",
        loanAmount=750000,
        loanInterest=4.5,
        accountStatus="Active"
    )
}


# API Endpoints
@app.get("/credits", response_model=List[CreditInfo])
def get_all_credits():
    return list(db.values())

@app.get("/credits/{credit_id}", response_model=CreditInfo)
def get_credit_by_id(credit_id: int):
    credit = db.get(credit_id)
    if credit is None:
        raise HTTPException(status_code=404, detail="Credit not found")
    return credit

@app.post("/credits", response_model=CreditInfo)
def create_credit(credit: CreditInfo):
    credit_id = max(db.keys(), default=0) + 1
    credit.id = credit_id
    db[credit_id] = credit
    return credit

@app.put("/credits/{credit_id}", response_model=CreditInfo)
def update_credit(credit_id: int, updated_credit: CreditInfo):
    if credit_id not in db:
        raise HTTPException(status_code=404, detail="Credit not found")
    db[credit_id] = updated_credit
    return updated_credit

@app.delete("/credits/{credit_id}", response_model=dict)
def delete_credit(credit_id: int):
    if credit_id not in db:
        raise HTTPException(status_code=404, detail="Credit not found")
    deleted_credit = db.pop(credit_id)
    return {"message": "Credit deleted successfully", "deleted_credit": deleted_credit}
