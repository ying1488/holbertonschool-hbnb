import app.models.review as Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):

    def __init__(self):
        super().__init__(Review)
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
