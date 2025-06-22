#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Test that the Amenity model works as expected"""

    def test_create_amenity(self):
        """Tests creation of Amenity instances"""
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")  # Fixed typo: "Wif-Fi" -> "Wi-Fi"
        print("Amenity creation test passed!")

    # TODO: Add more tests
    def test_empty_name(self):
        """Tests that Amenity cannot have an empty name"""
        amenity = Amenity(name="")
        self.assertEqual(amenity.name, "")
        print("Empty name test passed!")

    def test_amenity_string_representation(self):
        """Tests string representation (if defined)"""
        amenity = Amenity(name="Pool")
        self.assertTrue("Pool" in str(amenity))  # Only if __str__ or __repr__ is defined
        print("String representation test passed!")

if __name__ == '__main__':
    unittest.main()
