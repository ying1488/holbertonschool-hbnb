from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)  # Pass the model to the base class

    def get(self, place_id):
        return Place.query.filter_by(id=place_id).first()


    def add(self, new_place):
        db.session.add(new_place)
        db.session.commit()
        return new_place

    def all(self):
        return Place.query.all()

    def save(self, place_id, updated_place):
        place = Place.query.get(place_id)
        if place:
            for key, value in vars(updated_place).items():
                if key != 'id' and hasattr(place, key):
                    setattr(place, key, value)
            db.session.commit()
        return place
