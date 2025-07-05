from app.models.base_model import BaseModel
import uuid
from app import db, bcrypt

class Amenity(BaseModel):

    """Amenity class to represent amenities in the HBNB application."""

    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name
        
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
