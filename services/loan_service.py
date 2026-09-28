from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Employee, Key, KeyLoan
from schemas import LoanCreate, LoanReturn


class LoanNotFoundError(Exception):
    pass


class LoanConflictError(Exception):
    pass


class LoanService:
    def __init__(self, database: Session):
        self.database = database

    def issue_key(self, loan_data: LoanCreate) -> KeyLoan:
        key = self.database.get(Key, loan_data.key_id)
        employee = self.database.get(Employee, loan_data.employee_id)
        operator = self.database.get(Employee, loan_data.issued_by_operator_id)

        if key is None:
            raise LoanNotFoundError("Schlüssel nicht gefunden")
        if employee is None:
            raise LoanNotFoundError("Mitarbeiter nicht gefunden")
        if operator is None:
            raise LoanNotFoundError("Bediener nicht gefunden")
        if not employee.active:
            raise LoanConflictError("Mitarbeiter ist nicht aktiv")
        self._validate_operator(operator)
        if key.status != "available":
            raise LoanConflictError("Schlüssel ist nicht verfügbar")

        open_loan = self.database.scalar(
            select(KeyLoan).where(
                KeyLoan.key_id == key.id,
                KeyLoan.returned_at.is_(None),
            )
        )
        if open_loan is not None:
            raise LoanConflictError("Schlüssel ist bereits ausgeliehen")

        loan = KeyLoan(**loan_data.model_dump())
        key.status = "issued"
        self.database.add(loan)

        try:
            self.database.commit()
        except IntegrityError as error:
            self.database.rollback()
            raise LoanConflictError("Schlüssel ist bereits ausgeliehen") from error

        self.database.refresh(loan)
        return loan

    def return_key(self, loan_id: int, return_data: LoanReturn) -> KeyLoan:
        loan = self.database.get(KeyLoan, loan_id)
        operator = self.database.get(Employee, return_data.returned_by_operator_id)

        if loan is None:
            raise LoanNotFoundError("Ausleihe nicht gefunden")
        if operator is None:
            raise LoanNotFoundError("Bediener nicht gefunden")
        self._validate_operator(operator)
        if loan.returned_at is not None:
            raise LoanConflictError("Schlüssel wurde bereits zurückgegeben")

        loan.returned_by_operator_id = operator.id
        loan.returned_at = datetime.now(timezone.utc)
        loan.key.status = "available"
        self.database.commit()
        self.database.refresh(loan)
        return loan

    @staticmethod
    def _validate_operator(operator: Employee) -> None:
        if not operator.active or operator.role != "operator":
            raise LoanConflictError("Bediener ist nicht aktiv oder nicht berechtigt")
