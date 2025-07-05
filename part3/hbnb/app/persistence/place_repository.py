import app.models.place as Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Place)
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
