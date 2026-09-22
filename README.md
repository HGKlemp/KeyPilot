# KeyPilot

FastAPI-Backend zur Verwaltung von Schlüsseln, Räumen und Ausleihen.

## Installation

```powershell
python -m pip install -r requirements.txt
```

## Datenbanktabellen erstellen

```powershell
python create_database.py
```

## Testdaten eintragen

```powershell
python db_seed.py
```

`db_seed.py` trägt nur in eine leere Datenbank ein.

## Entwicklungsserver starten

```powershell
python -m uvicorn app:app --reload
```

Danach sind erreichbar:

- API: http://127.0.0.1:8000
- Swagger-Dokumentation: http://127.0.0.1:8000/docs
- Alternative API-Dokumentation: http://127.0.0.1:8000/redoc

## Datenbanktabellen löschen

```powershell
python drop_database.py
```

`drop_database.py` löscht alle von KeyPilot verwalteten Tabellen und Daten.
