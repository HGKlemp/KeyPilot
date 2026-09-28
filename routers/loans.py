from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from extensions import get_db
from repositories.loan_repository import LoanRepository
from schemas import LoanCreate, LoanRead, LoanReturn
from services.loan_service import LoanConflictError, LoanNotFoundError, LoanService


router = APIRouter(prefix="/loans", tags=["Loans"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[LoanRead])
def list_loans(database: DatabaseSession):
    return LoanRepository(database).get_all()


@router.get("/{loan_id}", response_model=LoanRead)
def get_loan(loan_id: int, database: DatabaseSession):
    loan = LoanRepository(database).get_by_id(loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    return loan


@router.post("", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def issue_key(loan_data: LoanCreate, database: DatabaseSession):
    try:
        return LoanService(database).issue_key(loan_data)
    except LoanNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except LoanConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.patch("/{loan_id}/return", response_model=LoanRead)
def return_key(
    loan_id: int,
    return_data: LoanReturn,
    database: DatabaseSession,
):
    try:
        return LoanService(database).return_key(loan_id, return_data)
    except LoanNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except LoanConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
