#!/usr/bin/python3
""" Unittests for HBnB Evolution v2 Part 2 """

import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    """Test that the User model works as expected
    """

    def test_create_user(self):
        """Tests creation of User instances """
        user = User(first_name="Peter", last_name="Parker", email="iluvspiderman@dailybugle.com")

        assert user.first_name == "Peter"
        assert user.last_name == "Parker"
        assert user.email == "iluvspiderman@dailybugle.com"
        assert user.is_admin is False  # Default value
        print("User creation test passed!")

    # TODO: add more tests

if __name__ == '__main__':
    unittest.main()
