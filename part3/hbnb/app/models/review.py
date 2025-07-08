from app.models.base_model import BaseModel
from app import db, bcrypt
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship

class Review(BaseModel):
    
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_r = relationship('Place', back_populates='review_r')
    author_r = relationship('User', back_populates='review_r')

    # Foreign keys
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Constraints - Check for rating range, from 1 to 5
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id
       
    def update_review(self, text=None, rating=None):
        """Update the review text and/or rating."""
        if text is not None:
            self.text = text
        if rating is not None:
            self.rating = rating
        db.session.commit()

    def delete_review(self):
        """Delete the review."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the review based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def __str__(self):
        """Return a string representation of the Review instance."""
        return (f"Review(text={self.text}, rating={self.rating}, "
                f"place_id={self.place_id}, user_id={self.user_id}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")
