# KeyPilot

Backend application for managing keys, rooms and key assignments.

## Datenbanktabellen erstellen

```powershell
python create_database.py
```

## Datenbanktabellen löschen

```powershell
python drop_database.py
```

`drop_database.py` löscht alle von KeyPilot verwalteten Tabellen und deren Daten. Anschließend können die Tabellen mit `create_database.py` neu erstellt werden.
