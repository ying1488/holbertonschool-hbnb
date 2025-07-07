from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app import db

class AmenityRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Amenity)

    def save(self, amenity):
        db.session.add(amenity)
        db.session.commit()
    
    def get(self, amenity_id):
        return self.model.query.get(amenity_id)

    def all(self):
        return self.model.query.all()
    
