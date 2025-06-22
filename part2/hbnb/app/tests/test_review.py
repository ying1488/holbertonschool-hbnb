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
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"})
        print("Response status:", UserResponse.status_code)
        print("Response data:", UserResponse.get_json())
        self.assertEqual(UserResponse.status_code, 201)
        self.user_id = json.loads(UserResponse.data)['id']
        
        # Create Place user
        PlaceResponse = self.client.post('/api/v1/places/', 
                                        json={
                                            "title": "Review Test Place",
                                            "description": "description",
                                            "price": 80.0,
                                            "latitude": 34.0522,
                                            "longitude": -118.2437,
                                            "owner_id": self.user_id,
                                            "amenities": []
                                        })
        self.place_id = json.loads(PlaceResponse.data)['id']
        print("Response status:", PlaceResponse.status_code)
        print("Response data:", PlaceResponse.get_json())
        self.assertEqual(PlaceResponse.status_code, 201)

         # Create Place user
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Awesome stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
            })
        self.assertEqual(review_response.status_code, 201)
        self.assertIn("id", review_response.get_json())


if __name__ == '__main__':
    unittest.main()