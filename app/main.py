from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import engine, get_db
from app.models import Base, LoanDB
from app.schemas import LoanCreate, LoanRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("/api/loans", response_model=LoanRead,
          status_code=status.HTTP_201_CREATED,
          )

def add_loan(new_loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = LoanDB(**new_loan.model.dump())
    db.add(db_loan)

    try:
        db.commit()
        db.refresh(db_loan)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A loan with this name or id already exists"
        )
    return db_loan

@app.get("/api/loans/{id}", response_model=LoanRead)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = db.get(LoanDB, loan_id)

    if db_loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return db_loan

