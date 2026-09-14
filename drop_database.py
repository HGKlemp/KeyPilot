from sqlalchemy import text

from app import app
from extensions import db


LEGACY_TABLES = ("loans", "operators", "alembic_version")


def drop_database():
    with app.app_context():
        for table_name in LEGACY_TABLES:
            db.session.execute(
                text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
            )

        db.session.commit()
        db.drop_all()


if __name__ == "__main__":
    drop_database()
    print("Alle KeyPilot-Tabellen wurden gelöscht.")
