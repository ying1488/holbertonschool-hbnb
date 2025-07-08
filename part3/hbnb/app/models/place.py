from app.models.base_model import BaseModel
from app import db, bcrypt
from sqlalchemy.orm import relationship
import uuid

import uuid

# Association table between places and amenities (many-to-many)
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):

    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    amenities_r = relationship('Amenity', secondary=place_amenities, back_populates='places_r')
    owner_r = relationship('User', back_populates='properties_r')
    review_r = relationship('Review', back_populates='place_r', cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner.id
        self.amenities = []
        self.reviews = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "amenities": [amenity.to_dict() for amenity in self.amenities_r]
        }

    
    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            db.session.commit()

    def add_review(self, review):
        self.reviews.append(review)
        db.session.commit()
     
    def update_title(self, title):
        self.title = title
        db.session.commit()

    def update_description(self, description):
        self.description = description
        db.session.commit()

    def update_price(self, price):
        self.price = price
        db.session.commit()
    
    def update_location(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        db.session.commit()

    def delete_place(self):
        """Delete the place and all associated reviews and amenities. To be updated as handled by cascade"""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the place based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def __str__(self):
        """Return a string representation of the Place instance."""
        return (f"Place(title={self.title}, description={self.description}, "
                f"price={self.price}, latitude={self.latitude}, "
                f"longitude={self.longitude}, owner={self.owner.id}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")
    