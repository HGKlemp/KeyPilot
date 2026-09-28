from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate


class EmployeeRepository:
    def __init__(self, database: Session):
        self.database = database

    def get_all(self) -> list[Employee]:
        statement = select(Employee).order_by(
            Employee.last_name,
            Employee.first_name,
        )
        return list(self.database.scalars(statement).all())

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.database.get(Employee, employee_id)

    def create(self, employee_data: EmployeeCreate) -> Employee:
        employee = Employee(**employee_data.model_dump())
        self.database.add(employee)
        self.database.commit()
        self.database.refresh(employee)
        return employee

    def update(
        self,
        employee: Employee,
        employee_data: EmployeeUpdate,
    ) -> Employee:
        for field, value in employee_data.model_dump(exclude_unset=True).items():
            setattr(employee, field, value)

        self.database.commit()
        self.database.refresh(employee)
        return employee
