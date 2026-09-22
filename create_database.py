import models
from extensions import Base, engine


def create_database():
    Base.metadata.create_all(bind=engine)
    return Base.metadata.sorted_tables


if __name__ == "__main__":
    created_tables = create_database()
    print("Datenbanktabellen wurden aus models.py erstellt:")

    for table in created_tables:
        columns = ", ".join(column.name for column in table.columns)
        print(f"- {table.name}: {columns}")
