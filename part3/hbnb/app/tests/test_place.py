#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

class TestPlace(unittest.TestCase):
    """Test that the Place model works as expected"""

    def test_create_place(self):
        """Tests creation of Place instance and adding a review"""
        owner = User(first_name="John", last_name="Smith", email="John.Smith@gmail.com")
        place = Place(
            title="Crozy Apartment",
            description="A nice place to stay.",
            price=100.00,
            latitude=40.7128,
            longitude=-74.0060,
            owner=owner
        )

        # Add review
        review = Review(text="Great Stay", rating=5)
        place.add_review(review)

        # Assertions
        self.assertEqual(place.title, "Crozy Apartment")
        self.assertEqual(place.price, 100.00)
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great Stay")
        print("✅ Place creation and relationship test passed!")

if __name__ == '__main__':
    unittest.main()
