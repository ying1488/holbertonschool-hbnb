from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class to represent amenities in the HBNB application."""
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        """Return a string representation of the Amenity instance."""
        return f"Amenity(name={self.name}, id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})"
    
    def update_name(self, name):
        """Update the name of the amenity."""
        self.name = name
        self.save()
    
    def delete_amenity(self):
        """Delete the amenity."""
        self.name = None
        self.id = None
        self.created_at = None
        self.updated_at = None
    
    def update(self, data):
        """Update the attributes of the amenity based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()