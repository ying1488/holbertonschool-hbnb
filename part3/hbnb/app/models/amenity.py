from app.models.base_model import BaseModel
import uuid
import re
from sqlalchemy.orm import relationship
from app import db, bcrypt
from app.models.place import place_amenities

class Amenity(BaseModel):

    """Amenity class to represent amenities in the HBNB application."""

    __tablename__ = 'amenities'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    places_r = relationship('Place', secondary=place_amenities, back_populates='amenities_r')

    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
    def update_name(self, name):
        """Bulk update amenity attributes from a dictionary."""
        self.name = name
        db.session.commit()
    
    def delete_amenity(self):
        """Delete the amenity."""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, data):
        """Update the attributes of the amenity based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def __str__(self):
        """Return a string representation of the Amenity instance."""
        return f"Amenity(name={self.name}, id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})"
