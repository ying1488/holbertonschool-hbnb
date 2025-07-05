import app.models.amenity as Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):

    def __init__(self):
        self._data = {}

    def save(self, amenity_id, amenity):
        self._data[amenity_id] = amenity
    
    def get(self, amenity_id):
        return self._data.get(amenity_id)

    def all(self):
        return self._data.values
