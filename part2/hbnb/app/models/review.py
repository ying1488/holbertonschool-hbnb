from base_model import BaseModel

class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def __str__(self):
        """Return a string representation of the Review instance."""
        return (f"Review(text={self.text}, rating={self.rating}, "
                f"place={self.place.id}, user={self.user.id}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")
    
    def update_review(self, text=None, rating=None):
        """Update the review text and/or rating."""
        if text is not None:
            self.text = text
        if rating is not None:
            self.rating = rating
        self.save()

    def delete_review(self):
        """Delete the review."""
        self.text = None
        self.rating = None
        self.place = None
        self.user = None
        self.id = None
        self.created_at = None
        self.updated_at = None
    