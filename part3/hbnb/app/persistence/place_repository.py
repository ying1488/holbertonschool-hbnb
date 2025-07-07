from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):

    def __init__(self):
        self._data = {}
    
    def get(self, owner_id):
        return self._data.get(owner_id)
    
    def add(self, new_place):
        db.session.add(new_place)
        db.session.commit()  # commit to generate ID
        return new_place
    
    def all(self):
        return self._data.values()
    
    def save(self, place_id, place):
        self._data[place_id] = place
