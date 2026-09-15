"""Trägt ausgeschriebene Testdaten in eine leere KeyPilot-Datenbank ein.
Datei im KeyPilot-Hauptordner ablegen und mit python db_seed.py starten.
"""
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent / ".env")

from app import app
from extensions import db
from models import Employee, Key, KeyLoan, Room

# Jede Zeile ist genau ein Mitarbeiter: Vorname, Nachname, E-Mail, Rolle, aktiv.
EMPLOYEES = [
    ("Anna", "Schmidt", "anna.schmidt@keypilot.de", "operator", True),
    ("Markus", "Weber", "markus.weber@keypilot.de", "operator", True),
    ("Julia", "Fischer", "julia.fischer@keypilot.de", "operator", True),
    ("Thomas", "Wagner", "thomas.wagner@keypilot.de", "employee", True),
    ("Laura", "Becker", "laura.becker@keypilot.de", "employee", True),
    ("Michael", "Hoffmann", "michael.hoffmann@keypilot.de", "employee", True),
    ("Sophie", "Schäfer", "sophie.schaefer@keypilot.de", "employee", True),
    ("Daniel", "Koch", "daniel.koch@keypilot.de", "employee", True),
    ("Katharina", "Bauer", "katharina.bauer@keypilot.de", "employee", True),
    ("Stefan", "Richter", "stefan.richter@keypilot.de", "employee", True),
    ("Marie", "Klein", "marie.klein@keypilot.de", "employee", True),
    ("Andreas", "Wolf", "andreas.wolf@keypilot.de", "employee", True),
    ("Lisa", "Schröder", "lisa.schroeder@keypilot.de", "employee", True),
    ("Christian", "Neumann", "christian.neumann@keypilot.de", "employee", True),
    ("Sarah", "Schwarz", "sarah.schwarz@keypilot.de", "employee", True),
    ("Martin", "Zimmermann", "martin.zimmermann@keypilot.de", "employee", True),
    ("Nina", "Braun", "nina.braun@keypilot.de", "employee", True),
    ("Sebastian", "Krüger", "sebastian.krueger@keypilot.de", "employee", True),
    ("Lea", "Hartmann", "lea.hartmann@keypilot.de", "employee", True),
    ("Florian", "Lange", "florian.lange@keypilot.de", "employee", True),
    ("Johanna", "Werner", "johanna.werner@keypilot.de", "employee", True),
    ("Patrick", "Schmitz", "patrick.schmitz@keypilot.de", "employee", True),
    ("Lena", "Krause", "lena.krause@keypilot.de", "employee", True),
    ("Tobias", "Meier", "tobias.meier@keypilot.de", "employee", True),
    ("Vanessa", "Lehmann", "vanessa.lehmann@keypilot.de", "employee", True),
    ("Jan", "Schmid", "jan.schmid@keypilot.de", "employee", True),
    ("Melanie", "Schulz", "melanie.schulz@keypilot.de", "employee", True),
    ("Alexander", "Maier", "alexander.maier@keypilot.de", "employee", True),
    ("Carolin", "Köhler", "carolin.koehler@keypilot.de", "employee", True),
    ("Felix", "Herrmann", "felix.herrmann@keypilot.de", "employee", True),
]

# Jede Zeile ist genau ein Raum: Raumnummer, Name, Gebäude, Etage, aktiv.
ROOMS = [
    ("A-001", "Büro 1", "Gebäude A", "0", True),
    ("A-002", "Besprechungsraum 2", "Gebäude A", "0", True),
    ("A-003", "Schulungsraum 3", "Gebäude A", "0", True),
    ("A-004", "Lager 4", "Gebäude A", "0", True),
    ("A-005", "Technikraum 5", "Gebäude A", "0", True),
    ("A-006", "Werkstatt 6", "Gebäude A", "0", True),
    ("A-007", "Archiv 7", "Gebäude A", "0", True),
    ("A-008", "Serverraum 8", "Gebäude A", "0", True),
    ("A-009", "Aufenthaltsraum 9", "Gebäude A", "0", True),
    ("A-010", "Verwaltung 10", "Gebäude A", "0", True),
    ("A-101", "Büro 11", "Gebäude A", "1", True),
    ("A-102", "Besprechungsraum 12", "Gebäude A", "1", True),
    ("A-103", "Schulungsraum 13", "Gebäude A", "1", True),
    ("A-104", "Lager 14", "Gebäude A", "1", True),
    ("A-105", "Technikraum 15", "Gebäude A", "1", True),
    ("A-106", "Werkstatt 16", "Gebäude A", "1", True),
    ("A-107", "Archiv 17", "Gebäude A", "1", True),
    ("A-108", "Serverraum 18", "Gebäude A", "1", True),
    ("A-109", "Aufenthaltsraum 19", "Gebäude A", "1", True),
    ("A-110", "Verwaltung 20", "Gebäude A", "1", True),
    ("A-201", "Büro 21", "Gebäude A", "2", True),
    ("A-202", "Besprechungsraum 22", "Gebäude A", "2", True),
    ("A-203", "Schulungsraum 23", "Gebäude A", "2", True),
    ("A-204", "Lager 24", "Gebäude A", "2", True),
    ("A-205", "Technikraum 25", "Gebäude A", "2", True),
    ("B-001", "Werkstatt 26", "Gebäude B", "0", True),
    ("B-002", "Archiv 27", "Gebäude B", "0", True),
    ("B-003", "Serverraum 28", "Gebäude B", "0", True),
    ("B-004", "Aufenthaltsraum 29", "Gebäude B", "0", True),
    ("B-005", "Verwaltung 30", "Gebäude B", "0", True),
    ("B-006", "Büro 31", "Gebäude B", "0", True),
    ("B-007", "Besprechungsraum 32", "Gebäude B", "0", True),
    ("B-008", "Schulungsraum 33", "Gebäude B", "0", True),
    ("B-009", "Lager 34", "Gebäude B", "0", True),
    ("B-010", "Technikraum 35", "Gebäude B", "0", True),
    ("B-101", "Werkstatt 36", "Gebäude B", "1", True),
    ("B-102", "Archiv 37", "Gebäude B", "1", True),
    ("B-103", "Serverraum 38", "Gebäude B", "1", True),
    ("B-104", "Aufenthaltsraum 39", "Gebäude B", "1", True),
    ("B-105", "Verwaltung 40", "Gebäude B", "1", True),
    ("B-106", "Büro 41", "Gebäude B", "1", True),
    ("B-107", "Besprechungsraum 42", "Gebäude B", "1", True),
    ("B-108", "Schulungsraum 43", "Gebäude B", "1", True),
    ("B-109", "Lager 44", "Gebäude B", "1", True),
    ("B-110", "Technikraum 45", "Gebäude B", "1", True),
    ("B-201", "Werkstatt 46", "Gebäude B", "2", True),
    ("B-202", "Archiv 47", "Gebäude B", "2", True),
    ("B-203", "Serverraum 48", "Gebäude B", "2", True),
    ("B-204", "Aufenthaltsraum 49", "Gebäude B", "2", True),
    ("B-205", "Verwaltung 50", "Gebäude B", "2", True),
]

# Jede Zeile ist genau ein Schlüssel: Nummer, Beschreibung, Lagerort, Status, Raumnummern.
KEYS = [
    ("S-001", "Schlüssel 001", "Schlüsselschrank, Fach 001", "available", ("A-001",)),
    ("S-002", "Schlüssel 002", "Schlüsselschrank, Fach 002", "available", ("A-002",)),
    ("S-003", "Schlüssel 003", "Schlüsselschrank, Fach 003", "available", ("A-003",)),
    ("S-004", "Schlüssel 004", "Schlüsselschrank, Fach 004", "available", ("A-004",)),
    ("S-005", "Schlüssel 005", "Schlüsselschrank, Fach 005", "available", ("A-005",)),
    ("S-006", "Schlüssel 006", "Schlüsselschrank, Fach 006", "available", ("A-006",)),
    ("S-007", "Schlüssel 007", "Schlüsselschrank, Fach 007", "available", ("A-007",)),
    ("S-008", "Schlüssel 008", "Schlüsselschrank, Fach 008", "available", ("A-008",)),
    ("S-009", "Schlüssel 009", "Schlüsselschrank, Fach 009", "available", ("A-009",)),
    ("S-010", "Schlüssel 010", "Schlüsselschrank, Fach 010", "available", ("A-010",)),
    ("S-011", "Schlüssel 011", "Schlüsselschrank, Fach 011", "available", ("A-101",)),
    ("S-012", "Schlüssel 012", "Schlüsselschrank, Fach 012", "available", ("A-102",)),
    ("S-013", "Schlüssel 013", "Schlüsselschrank, Fach 013", "available", ("A-103",)),
    ("S-014", "Schlüssel 014", "Schlüsselschrank, Fach 014", "available", ("A-104",)),
    ("S-015", "Schlüssel 015", "Schlüsselschrank, Fach 015", "available", ("A-105",)),
    ("S-016", "Schlüssel 016", "Schlüsselschrank, Fach 016", "available", ("A-106",)),
    ("S-017", "Schlüssel 017", "Schlüsselschrank, Fach 017", "available", ("A-107",)),
    ("S-018", "Schlüssel 018", "Schlüsselschrank, Fach 018", "available", ("A-108",)),
    ("S-019", "Schlüssel 019", "Schlüsselschrank, Fach 019", "available", ("A-109",)),
    ("S-020", "Schlüssel 020", "Schlüsselschrank, Fach 020", "available", ("A-110",)),
    ("S-021", "Schlüssel 021", "Schlüsselschrank, Fach 021", "available", ("A-201",)),
    ("S-022", "Schlüssel 022", "Schlüsselschrank, Fach 022", "available", ("A-202",)),
    ("S-023", "Schlüssel 023", "Schlüsselschrank, Fach 023", "available", ("A-203",)),
    ("S-024", "Schlüssel 024", "Schlüsselschrank, Fach 024", "available", ("A-204",)),
    ("S-025", "Schlüssel 025", "Schlüsselschrank, Fach 025", "available", ("A-205",)),
    ("S-026", "Schlüssel 026", "Schlüsselschrank, Fach 026", "available", ("B-001",)),
    ("S-027", "Schlüssel 027", "Schlüsselschrank, Fach 027", "available", ("B-002",)),
    ("S-028", "Schlüssel 028", "Schlüsselschrank, Fach 028", "available", ("B-003",)),
    ("S-029", "Schlüssel 029", "Schlüsselschrank, Fach 029", "available", ("B-004",)),
    ("S-030", "Schlüssel 030", "Schlüsselschrank, Fach 030", "available", ("B-005",)),
    ("S-031", "Schlüssel 031", "Schlüsselschrank, Fach 031", "available", ("B-006",)),
    ("S-032", "Schlüssel 032", "Schlüsselschrank, Fach 032", "available", ("B-007",)),
    ("S-033", "Schlüssel 033", "Schlüsselschrank, Fach 033", "available", ("B-008",)),
    ("S-034", "Schlüssel 034", "Schlüsselschrank, Fach 034", "available", ("B-009",)),
    ("S-035", "Schlüssel 035", "Schlüsselschrank, Fach 035", "available", ("B-010",)),
    ("S-036", "Schlüssel 036", "Schlüsselschrank, Fach 036", "available", ("B-101",)),
    ("S-037", "Schlüssel 037", "Schlüsselschrank, Fach 037", "available", ("B-102",)),
    ("S-038", "Schlüssel 038", "Schlüsselschrank, Fach 038", "available", ("B-103",)),
    ("S-039", "Schlüssel 039", "Schlüsselschrank, Fach 039", "available", ("B-104",)),
    ("S-040", "Schlüssel 040", "Schlüsselschrank, Fach 040", "available", ("B-105",)),
    ("S-041", "Schlüssel 041", "Schlüsselschrank, Fach 041", "available", ("B-106",)),
    ("S-042", "Schlüssel 042", "Schlüsselschrank, Fach 042", "available", ("B-107",)),
    ("S-043", "Schlüssel 043", "Schlüsselschrank, Fach 043", "available", ("B-108",)),
    ("S-044", "Schlüssel 044", "Schlüsselschrank, Fach 044", "available", ("B-109",)),
    ("S-045", "Schlüssel 045", "Schlüsselschrank, Fach 045", "available", ("B-110",)),
    ("S-046", "Schlüssel 046", "Schlüsselschrank, Fach 046", "available", ("B-201",)),
    ("S-047", "Schlüssel 047", "Schlüsselschrank, Fach 047", "available", ("B-202",)),
    ("S-048", "Schlüssel 048", "Schlüsselschrank, Fach 048", "available", ("B-203",)),
    ("S-049", "Schlüssel 049", "Schlüsselschrank, Fach 049", "available", ("B-204",)),
    ("S-050", "Schlüssel 050", "Schlüsselschrank, Fach 050", "available", ("B-205",)),
    ("S-051", "Schlüssel 051", "Schlüsselschrank, Fach 051", "available", ("A-001", "A-002")),
    ("S-052", "Schlüssel 052", "Schlüsselschrank, Fach 052", "available", ("A-003", "A-004")),
    ("S-053", "Schlüssel 053", "Schlüsselschrank, Fach 053", "available", ("A-005", "A-006")),
    ("S-054", "Schlüssel 054", "Schlüsselschrank, Fach 054", "available", ("A-007", "A-008")),
    ("S-055", "Schlüssel 055", "Schlüsselschrank, Fach 055", "available", ("A-009", "A-010")),
    ("S-056", "Schlüssel 056", "Schlüsselschrank, Fach 056", "available", ("A-101", "A-102")),
    ("S-057", "Schlüssel 057", "Schlüsselschrank, Fach 057", "available", ("A-103", "A-104")),
    ("S-058", "Schlüssel 058", "Schlüsselschrank, Fach 058", "available", ("A-105", "A-106")),
    ("S-059", "Schlüssel 059", "Schlüsselschrank, Fach 059", "available", ("A-107", "A-108")),
    ("S-060", "Schlüssel 060", "Schlüsselschrank, Fach 060", "available", ("A-109", "A-110")),
    ("S-061", "Schlüssel 061", "Schlüsselschrank, Fach 061", "available", ("A-201", "A-202")),
    ("S-062", "Schlüssel 062", "Schlüsselschrank, Fach 062", "available", ("A-203", "A-204")),
    ("S-063", "Schlüssel 063", "Schlüsselschrank, Fach 063", "available", ("A-205", "B-001")),
    ("S-064", "Schlüssel 064", "Schlüsselschrank, Fach 064", "available", ("B-002", "B-003")),
    ("S-065", "Schlüssel 065", "Schlüsselschrank, Fach 065", "available", ("B-004", "B-005")),
    ("S-066", "Schlüssel 066", "Schlüsselschrank, Fach 066", "available", ("B-006", "B-007")),
    ("S-067", "Schlüssel 067", "Schlüsselschrank, Fach 067", "available", ("B-008", "B-009")),
    ("S-068", "Schlüssel 068", "Schlüsselschrank, Fach 068", "available", ("B-010", "B-101")),
    ("S-069", "Schlüssel 069", "Schlüsselschrank, Fach 069", "available", ("B-102", "B-103")),
    ("S-070", "Schlüssel 070", "Schlüsselschrank, Fach 070", "available", ("B-104", "B-105")),
    ("S-071", "Hauptschlüssel Gebäude A", "Schlüsselschrank, Fach 071", "available", ("A-001", "A-002", "A-003", "A-004", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "A-101", "A-102", "A-103", "A-104", "A-105", "A-106", "A-107", "A-108", "A-109", "A-110", "A-201", "A-202", "A-203", "A-204", "A-205")),
    ("S-072", "Hauptschlüssel Gebäude A", "Schlüsselschrank, Fach 072", "available", ("A-001", "A-002", "A-003", "A-004", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "A-101", "A-102", "A-103", "A-104", "A-105", "A-106", "A-107", "A-108", "A-109", "A-110", "A-201", "A-202", "A-203", "A-204", "A-205")),
    ("S-073", "Hauptschlüssel Gebäude A", "Schlüsselschrank, Fach 073", "available", ("A-001", "A-002", "A-003", "A-004", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "A-101", "A-102", "A-103", "A-104", "A-105", "A-106", "A-107", "A-108", "A-109", "A-110", "A-201", "A-202", "A-203", "A-204", "A-205")),
    ("S-074", "Hauptschlüssel Gebäude A", "Schlüsselschrank, Fach 074", "available", ("A-001", "A-002", "A-003", "A-004", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "A-101", "A-102", "A-103", "A-104", "A-105", "A-106", "A-107", "A-108", "A-109", "A-110", "A-201", "A-202", "A-203", "A-204", "A-205")),
    ("S-075", "Hauptschlüssel Gebäude A", "Schlüsselschrank, Fach 075", "available", ("A-001", "A-002", "A-003", "A-004", "A-005", "A-006", "A-007", "A-008", "A-009", "A-010", "A-101", "A-102", "A-103", "A-104", "A-105", "A-106", "A-107", "A-108", "A-109", "A-110", "A-201", "A-202", "A-203", "A-204", "A-205")),
    ("S-076", "Hauptschlüssel Gebäude B", "Schlüsselschrank, Fach 076", "available", ("B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-101", "B-102", "B-103", "B-104", "B-105", "B-106", "B-107", "B-108", "B-109", "B-110", "B-201", "B-202", "B-203", "B-204", "B-205")),
    ("S-077", "Hauptschlüssel Gebäude B", "Schlüsselschrank, Fach 077", "available", ("B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-101", "B-102", "B-103", "B-104", "B-105", "B-106", "B-107", "B-108", "B-109", "B-110", "B-201", "B-202", "B-203", "B-204", "B-205")),
    ("S-078", "Hauptschlüssel Gebäude B", "Schlüsselschrank, Fach 078", "available", ("B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-101", "B-102", "B-103", "B-104", "B-105", "B-106", "B-107", "B-108", "B-109", "B-110", "B-201", "B-202", "B-203", "B-204", "B-205")),
    ("S-079", "Hauptschlüssel Gebäude B", "Schlüsselschrank, Fach 079", "available", ("B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-101", "B-102", "B-103", "B-104", "B-105", "B-106", "B-107", "B-108", "B-109", "B-110", "B-201", "B-202", "B-203", "B-204", "B-205")),
    ("S-080", "Hauptschlüssel Gebäude B", "Schlüsselschrank, Fach 080", "available", ("B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008", "B-009", "B-010", "B-101", "B-102", "B-103", "B-104", "B-105", "B-106", "B-107", "B-108", "B-109", "B-110", "B-201", "B-202", "B-203", "B-204", "B-205")),
]


def seed_database():
    with app.app_context():
        counts = {
            "Mitarbeiter": db.session.query(Employee).count(),
            "Räume": db.session.query(Room).count(),
            "Schlüssel": db.session.query(Key).count(),
            "Ausleihen": db.session.query(KeyLoan).count(),
        }
        if any(counts.values()):
            details = ", ".join(f"{name}: {count}" for name, count in counts.items() if count)
            raise RuntimeError(f"Datenbank enthält bereits Daten; nichts eingetragen. {details}")

        employees = [
            Employee(first_name=first_name, last_name=last_name, email=email, role=role, active=active)
            for first_name, last_name, email, role, active in EMPLOYEES
        ]
        rooms = [
            Room(room_number=number, name=name, building=building, floor=floor, active=active)
            for number, name, building, floor, active in ROOMS
        ]
        rooms_by_number = {room.room_number: room for room in rooms}
        keys = []
        for number, description, storage_location, status, room_numbers in KEYS:
            key = Key(key_number=number, description=description, storage_location=storage_location, status=status)
            key.rooms.extend(rooms_by_number[room_number] for room_number in room_numbers)
            keys.append(key)

        try:
            db.session.add_all(employees + rooms + keys)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        print(f"Eingetragen: {len(employees)} Mitarbeiter (3 Bediener), {len(rooms)} Räume, {len(keys)} Schlüssel.")
        print("Ausleihen: 0")


if __name__ == "__main__":
    seed_database() 