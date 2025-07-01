#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """
import unittest
import json
from app import create_app
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

#python3 -m unittest app.tests.test_review 

class TestReview(unittest.TestCase):
    """Test that the Review model works as expected
    To Run the test: #python3 -m unittest app.tests.test_review 
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
        ReviewResponse = self.client.post('/api/v1/reviews/', json={
            "text": "Awesome stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
            })
        print("Response status:", ReviewResponse.status_code)
        print("Response data:", ReviewResponse.get_json())
        self.assertEqual(ReviewResponse.status_code, 201)

def  test_create_review_InvalidLength(self):
    """Test review with no text"""
    res = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
    self.assertEqual(res.status_code, 400)

def  test_create_review_ExceedLength(self):
    """Test review with more than 200 words"""
    res = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet.Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi a tellus consequat imperdiet. Vestibulum sapien. Proin quam. Etiam ultrices. Suspendisse in justo eu magna luctus suscipit. Sed lectus. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. Praesent blandit dolor.Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas et, augue. Vestibulum convallis felis at dui. Nunc felis. Mauris dictum facilisis augue. Fusce tellus. Pellentesque dapibus elit ut et. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. Praesent blandit dolor.Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas et, augue. Vestibulum convallis felis at dui. Nunc felis. Mauris dictum facilisis augue. Fusce tellus. Pellentesque dapibus elit ut et. Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor, sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia molestie dui. Praesent blandit dolor.",
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
    self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()