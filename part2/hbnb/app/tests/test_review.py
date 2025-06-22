#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
import json
from app import create_app
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

class TestReview(unittest.TestCase):
    """Test that the Review model works as expected
    """

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        """Test creation of Review instances"""
        # Create test user
        UserResponse = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@example.com"})
        self.user.id = json.loads(UserResponse.data)['id']

        # Create test place
        PlaceResponse = self.client.post('/api/v1/places/',json)
