import unittest

from fastapi.testclient import TestClient

from app import app


class KeyApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_list_and_get_keys(self):
        list_response = self.client.get("/keys")

        self.assertEqual(list_response.status_code, 200)
        keys = list_response.json()
        self.assertEqual(len(keys), 80)
        self.assertEqual(keys[0]["key_number"], "S-001")
        self.assertIn("rooms", keys[0])

        detail_response = self.client.get(f"/keys/{keys[0]['id']}")

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["id"], keys[0]["id"])

    def test_missing_key_returns_404(self):
        response = self.client.get("/keys/999999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Schlüssel nicht gefunden")

    def test_create_key_rejects_issued_status(self):
        response = self.client.post(
            "/keys",
            json={
                "key_number": "TEST-NOT-SAVED",
                "status": "issued",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"],
            "Der Status 'issued' wird nur durch eine Ausleihe gesetzt",
        )

    def test_create_key_rejects_duplicate_number(self):
        existing_key = self.client.get("/keys").json()[0]
        response = self.client.post(
            "/keys",
            json={"key_number": existing_key["key_number"]},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"],
            "Schlüsselnummer ist bereits vergeben",
        )

    def test_patch_missing_key_returns_404(self):
        response = self.client.patch(
            "/keys/999999",
            json={"description": "Nicht vorhanden"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Schlüssel nicht gefunden")

    def test_key_status_issued_cannot_be_set_manually(self):
        keys = self.client.get("/keys").json()
        available_key = next(key for key in keys if key["status"] == "available")
        response = self.client.patch(
            f"/keys/{available_key['id']}",
            json={"status": "issued"},
        )

        self.assertEqual(response.status_code, 409)

    def test_key_status_is_validated(self):
        response = self.client.patch(
            "/keys/1",
            json={"status": "invalid"},
        )

        self.assertEqual(response.status_code, 422)

    def test_list_and_get_employees(self):
        list_response = self.client.get("/employees")

        self.assertEqual(list_response.status_code, 200)
        employees = list_response.json()
        self.assertGreater(len(employees), 0)
        self.assertIn("email", employees[0])
        self.assertIn("role", employees[0])

        detail_response = self.client.get(f"/employees/{employees[0]['id']}")

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["id"], employees[0]["id"])

    def test_missing_employee_returns_404(self):
        response = self.client.get("/employees/999999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Mitarbeiter nicht gefunden")

    def test_employee_role_is_validated(self):
        response = self.client.post(
            "/employees",
            json={
                "first_name": "Test",
                "last_name": "Person",
                "email": "test.person@KeyPilot.de",
                "role": "invalid",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_list_and_get_rooms(self):
        list_response = self.client.get("/rooms")

        self.assertEqual(list_response.status_code, 200)
        rooms = list_response.json()
        self.assertEqual(len(rooms), 50)
        self.assertEqual(rooms[0]["room_number"], "A-001")

        detail_response = self.client.get(f"/rooms/{rooms[0]['id']}")

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()["id"], rooms[0]["id"])

    def test_missing_room_returns_404(self):
        response = self.client.get("/rooms/999999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Raum nicht gefunden")

    def test_list_loans_and_missing_loan(self):
        list_response = self.client.get("/loans")

        self.assertEqual(list_response.status_code, 200)
        self.assertIsInstance(list_response.json(), list)

        detail_response = self.client.get("/loans/999999")

        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(detail_response.json()["detail"], "Ausleihe nicht gefunden")

    def test_room_and_loan_inputs_are_validated(self):
        room_response = self.client.post(
            "/rooms",
            json={"room_number": "", "name": ""},
        )
        loan_response = self.client.post(
            "/loans",
            json={
                "key_id": 0,
                "employee_id": 0,
                "issued_by_operator_id": 0,
            },
        )

        self.assertEqual(room_response.status_code, 422)
        self.assertEqual(loan_response.status_code, 422)

    def test_issue_missing_key_returns_404(self):
        response = self.client.post(
            "/loans",
            json={
                "key_id": 999999,
                "employee_id": 1,
                "issued_by_operator_id": 1,
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Schlüssel nicht gefunden")

    def test_return_missing_loan_returns_404(self):
        response = self.client.patch(
            "/loans/999999/return",
            json={"returned_by_operator_id": 1},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Ausleihe nicht gefunden")


if __name__ == "__main__":
    unittest.main()
