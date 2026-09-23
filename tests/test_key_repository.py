import unittest

from extensions import SessionLocal
from repositories.key_repository import KeyRepository


class KeyRepositoryIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.database = SessionLocal()
        self.repository = KeyRepository(self.database)

    def tearDown(self):
        self.database.close()

    def test_get_all_returns_sorted_keys(self):
        keys = self.repository.get_all()

        self.assertGreater(len(keys), 0)
        key_numbers = [key.key_number for key in keys]
        self.assertEqual(key_numbers, sorted(key_numbers))

    def test_get_by_id_returns_existing_key(self):
        expected_key = self.repository.get_all()[0]

        found_key = self.repository.get_by_id(expected_key.id)

        self.assertIsNotNone(found_key)
        self.assertEqual(found_key.id, expected_key.id)
        self.assertEqual(found_key.key_number, expected_key.key_number)

    def test_get_by_id_returns_none_for_missing_key(self):
        found_key = self.repository.get_by_id(-1)

        self.assertIsNone(found_key)


if __name__ == "__main__":
    unittest.main()
