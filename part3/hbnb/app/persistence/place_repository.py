from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get(self, place_id):
        return Place.query.get(place_id)

    def add(self, new_place):
        db.session.add(new_place)
        db.session.commit()
        return new_place

    def all(self):
        return Place.query.all()

    def save(self, place_id, place):
        db.session.commit()
        return place
