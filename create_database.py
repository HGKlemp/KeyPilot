import models
from app import app
from extensions import db


def create_database():
    with app.app_context():
        db.create_all()

    return db.metadata.sorted_tables


if __name__ == "__main__":
    created_tables = create_database()
    print("Datenbanktabellen wurden aus models.py erstellt:")

    for table in created_tables:
        columns = ", ".join(column.name for column in table.columns)
        print(f"- {table.name}: {columns}")
