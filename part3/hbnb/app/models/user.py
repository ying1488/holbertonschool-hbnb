from app.models.base_model import BaseModel
from app.extensions import db, bcrypt
import uuid
import re
from sqlalchemy.orm import relationship

class User(BaseModel):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    review_r = relationship("Review", back_populates="author_r")
    properties_r = relationship("Place", back_populates="owner_r")

    def __init__(self, first_name, last_name, email, password, is_admin=False):

        if first_name is None or first_name == "":
            raise ValueError("Please provide a first name")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        if isinstance(first_name, str) is False:
            raise ValueError("First name cannot be a number")

        if last_name is None or last_name == "":
            raise ValueError("Please provide a last name")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        if isinstance(last_name, str) is False:
            raise ValueError("Last name cannot be a number")

        if email is None:
            raise ValueError("Please provide an email")
        if email.count('@') != 1:
            raise ValueError("Email is not valid")
        if len(email) > 100:
            raise ValueError("Email cannot exceed 100 characters")

        if password is None or password == "":
            raise ValueError("Please provide a password")

        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place):
        self.places.append(place)
        self.save()

    def hash_password(self, password):
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        """Return a string representation of the User instance."""
        return (f"User(first_name={self.first_name}, last_name={self.last_name}, "
                f"email={self.email}, is_admin={self.is_admin}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def update_name(self, first_name=None, last_name=None):


        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        if isinstance(first_name, str) is False:
            raise ValueError("First name cannot be a number")

        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        if isinstance(last_name, str) is False:
            raise ValueError("Last name cannot be a number")

        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.save()

    def update_email(self, email):

        if email is None:
            raise ValueError("Please provide an email")
        if email.count('@') != 1:
            raise ValueError("Email is not valid")
        if len(email) > 100:
            raise ValueError("Email cannot exceed 100 characters")

        self.email = email
        self.save()
    
    def delete_place(self, place):
        if place in self.places:
            self.places.remove(place)
            self.save()
        else:
            print("Place not found in user's places.")

    def delete_account(self):
        for place in self.places:
            place.delete()
        self.places.clear()
        self.first_name = None
        self.last_name = None
        self.email = None
        self.is_admin = False
        self.id = None
        self.created_at = None
        self.updated_at = None
    
    def update(self, data):
        return super().update(data)
