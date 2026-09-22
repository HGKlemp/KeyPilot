from sqlalchemy import text

import models
from extensions import Base, engine


LEGACY_TABLES = ("loans", "operators", "alembic_version")


def drop_database():
    with engine.begin() as connection:
        for table_name in LEGACY_TABLES:
            connection.execute(
                text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
            )

    Base.metadata.drop_all(bind=engine)

    with engine.begin() as connection:
        connection.execute(text("DROP TYPE IF EXISTS loan_status"))


if __name__ == "__main__":
    drop_database()
    print("Alle KeyPilot-Tabellen wurden gelöscht.")
