from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from extensions import get_db
from repositories.employee_repository import EmployeeRepository
from schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate


router = APIRouter(prefix="/employees", tags=["Employees"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[EmployeeRead])
def list_employees(database: DatabaseSession):
    repository = EmployeeRepository(database)
    return repository.get_all()


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, database: DatabaseSession):
    repository = EmployeeRepository(database)
    employee = repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Mitarbeiter nicht gefunden")

    return employee


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee_data: EmployeeCreate, database: DatabaseSession):
    repository = EmployeeRepository(database)

    try:
        return repository.create(employee_data)
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-Mail-Adresse oder Auth0-ID ist bereits vergeben",
        ) from error


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    database: DatabaseSession,
):
    repository = EmployeeRepository(database)
    employee = repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Mitarbeiter nicht gefunden")

    try:
        return repository.update(employee, employee_data)
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(
            status_code=409,
            detail="E-Mail-Adresse oder Auth0-ID ist bereits vergeben",
        ) from error
