#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Test that the Amenity model works as expected
    """

def test_create_amenity(self):
        """Tests creation of Amenity instances """

        amenity = Amenity(name="Wi-Fi")
        assert amenity.name == "Wif-Fi"
        print("Amenity creation test passed!")

    # TODO: add more tests

if __name__ == '__main__':
    unittest.main()
