import app.models.amenity as Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Amenity)
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
