#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

class TestAmenity(unittest.TestCase):
    """Test that the Place model works as expected
    """

def test_create_place(self):
        """Tests creation of Place instances """
        owner = User(first_name="John", last_name="Smith", email="John.Smith@gmail.com")
        place = Place(title="Crozy Apartment", description="A nice place to stay.")

        # Add review ????
        review = Review(text="Great Stay", rating=5)
        place.add_review(review)

        assert place.title == "Crozy Apartment"
        assert place.price == 100.00
        assert len(place.reviews) == 1
        assert place.reviews[0].text == "Great stay"
        print("Place creation and relationship test passed!")

    # TODO: add more tests

if __name__ == '__main__':
    unittest.main()
