from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):

    def __init__(self):
        self._data = {}

    def get(self, review_data):
        return self.get(review_data)
    
    def add(self, review):
        self._data[review.id] = review
        return review

    def all(self):
        return list(self._data.values())

    def get_by_attribute(self, place_id):
        return [review for review in self._data.values() if review.place_id == place_id]
    
    def update(self, review_id, review_data):
        review = self.get(review_id)
        if review:
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            return review
        return None

    def delete(self, review_id):
        return self._data.pop(review_id, None)
