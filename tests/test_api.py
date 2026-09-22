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


if __name__ == "__main__":
    unittest.main()
