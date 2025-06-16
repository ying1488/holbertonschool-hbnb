from app.models.base_model import BaseModel


class Place(BaseModel):

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = []
        self.reviews = []
    
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
        self.save()

    def add_review(self, review):
        self.reviews.append(review)
        self.save()

    def __str__(self):
        """Return a string representation of the Place instance."""
        return (f"Place(title={self.title}, description={self.description}, "
                f"price={self.price}, latitude={self.latitude}, "
                f"longitude={self.longitude}, owner={self.owner.id}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")
    
    def update_title(self, title):
        self.title = title
        self.save()

    def update_description(self, description):
        self.description = description
        self.save()

    def update_price(self, price):
        self.price = price
        self.save()
    
    def update_location(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.save()

    def delete_place(self):
        """Delete the place and all associated reviews and amenities."""
        for review in self.reviews:
            review.delete_review()
        self.reviews.clear()
        
        for amenity in self.amenities:
            self.amenities.remove(amenity)
        
        self.title = None
        self.description = None
        self.price = None
        self.latitude = None
        self.longitude = None
        self.owner = None
        self.id = None
        self.created_at = None
        self.updated_at = None

    def update(self, data):
        """Update the attributes of the place based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass
