#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app import create_app

class TestUser(unittest.TestCase):
    """Test that the User model works as expected
    """

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        print("Response status:", response.status_code)
        print("Response data:", response.get_json())
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        print("Response status:", response.status_code)
        print("Response data:", response.get_json())
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vega",
            "last_name": "Balrog",
            "email": "invalid-email"
        })
        print("Response status:", response.status_code)
        print("Response data:", response.get_json())
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_name_num(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "jkdhajkshdjkashdjkahsjkdhjkashdjkashdkjhajksdhkjashdjkahsjkdhasjkdhajskhdahsjkhdak",
            "last_name": "Balrog",
            "email": "streetfighter@gmail.com"
        })
        print("Response status:", response.status_code)
        print("Response data:", response.get_json())
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
