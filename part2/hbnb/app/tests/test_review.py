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

    def test_create_review(self):
        """Test creation of Review instances"""
        # Create test user
        UserResponse = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"})
        self.user.id = json.loads(UserResponse.data)['id']

        # Create test place
        PlaceResponse = self.client.post('/api/v1/places/', json={
            "title": "Review Test Place",
            "price": 80.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.place_id = json.loads(PlaceResponse.data)['id']

    def test_create_review_success(self):
        """Test successful review creation"""
        res = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Great place to stay!",
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertIn('id', data)
        self.assertEqual(data['test'], 'Great place to stay!')
        self.assertEqual(data['rating'], 5)
    
if __name__ == '__main__':
    unittest.main()