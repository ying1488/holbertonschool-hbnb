from base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class to represent amenities in the HBNB application."""
    def __init__(self, name):
        super().__init__()
        self.name = name

