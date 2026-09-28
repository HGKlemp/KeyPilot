from sqlalchemy import select
from sqlalchemy.orm import Session

from models import KeyLoan


class LoanRepository:
    def __init__(self, database: Session):
        self.database = database

    def get_all(self) -> list[KeyLoan]:
        statement = select(KeyLoan).order_by(KeyLoan.issued_at.desc())
        return list(self.database.scalars(statement).all())

    def get_by_id(self, loan_id: int) -> KeyLoan | None:
        return self.database.get(KeyLoan, loan_id)
