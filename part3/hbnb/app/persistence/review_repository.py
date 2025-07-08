from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)  # <-- pass the model to the base class

    def get(self, review_id):
        return Review.query.get(review_id)

    def add(self, review):
        db.session.add(review)
        db.session.commit()
        return review

    def all(self):
        return Review.query.all()

    def get_by_attribute(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def update(self, review_id, review_data):
        review = Review.query.get(review_id)
        if review:
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            db.session.commit()
        return review

    def delete(self, review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
        return review
