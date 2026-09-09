import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import URL

from extensions import db
import models


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    print("Datenbanktabellen wurden geprüft/erstellt.")