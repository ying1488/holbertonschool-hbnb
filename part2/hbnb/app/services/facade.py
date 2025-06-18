import uuid
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class InvalidPlaceDataError(Exception):
    """Raised when place data is invalid."""

class PlaceNotFoundError(Exception):
    """Raised when a place with the given ID is not found."""

class InvalidPlaceUpdateError(Exception):
    pass

class InvalidReviewDataError(Exception):
    """Custom exception for invalid review data."""
    pass

class InvalidReviewUpdateError(Exception):
    """Custom exception for invalid review data update"""
    pass

class HBnBFacade:
    def __init__(self):
                 
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return list(self.user_repo.all().values())
    
    def update_user_name(self, user_id, first_name=None, last_name=None):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        self.user_repo.save(user_id, user)
        return {"message": "User name updated successfully"}
    
    def update_user_email(self, user_id, email):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.email = email
        self.user_repo.save(user_id, user)
        return {"message": "User email updated successfully"}
    
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.user_repo.save(user_id, user)
        return user

    # ---------- AMENITIES ----------
    
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required")
        amenity_id = str(uuid.uuid4())
        amenity = {
            'id': amenity_id,
            'name': name
        }
        self.amenity_repo.save(amenity_id, amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        amenity = self.amenity_repo.get(amenity_id)
        return amenity

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return list(self.amenity_repo.all().values())

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required")
        amenity['name'] = name
        self.amenity_repo.save(amenity_id, amenity)
        return {"message": "Amenity updated successfully"}
    
    # ---------- PLACES ----------

    def create_place(self, place_data):
        # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        try:
            new_place = Place(**place_data)
            self.place_repo.add(new_place)
            return new_place
        except ValueError as e:
            raise InvalidPlaceDataError(f"Invalid data: {str(e)}") from e

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner_id)
        amenities = [
        self.amenity_repo.get(amenity_id)
        for amenity_id in getattr(place, "amenities", [])
        if self.amenity_repo.get(amenity_id)
        ]

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            },
            "amenities": [{"id": a.id, "name": a.name} for a in amenities if a]
        }

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude
            }
            for p in self.place_repo.all().values()
        ]

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            for key, value in place_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            self.place_repo.save(place_id, place)
            return place
        except ValueError as e:
            raise InvalidPlaceUpdateError(f"Invalid update data: {str(e)}") from e
 
    # ---------- REVIEWS ----------

def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
    required_fields= ['user_id', 'place_id', 'rating']

    #Check required fields
    for field in required_fields:
        if field not in review_data:
            raise InvalidReviewDataError(f"Missing required:{field}")
    
    user_id = review_data.get('user_id')
    place_id = review_data.get('place_id')
    rating = review_data.get('rating')

    #Validate user and place exist
    user = self.user_repo.get(user_id)
    if not user:
        raise InvalidReviewDataError(f"User with id '{user_id}' not found.")
    
    place = self.place_repo.get(place_id)
    if not place: 
        raise InvalidReviewDataError(f"Place with id '{place_id}  not found.")
    # Validate rating 
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        raise InvalidReviewDataError("Rating must be an included")

    try:
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review
    except ValueError as e:
        raise InvalidReviewDataError(f"Invalid data: {str(e)}") from e

def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
    review = self.review_repo.get(review_id)
    if not review:
        return None
    owner = self.user_repo.get(review.owner_id)

    return {
        "id":review.id,
        "text": review.text,
        "rating": review.rating,
        "owner":{

        }
    }

def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
    return[
        {
            "id": r.id,
            "title": r.title,
            "latitude": r.latitude,
            "longitude": r.longitude
        }
        for r in self.review_repo.all().values()
    ]

def get_reviews_by_place(self, place_id):
    return self.review_repo.get_by_attribute('place_id', place_id)

def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if not review:
            return None

        try:
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            self.place_repo.save(review_id, place)
            return review
        except ValueError as e:
            raise InvalidReviewUpdateError(f"Invalid update data: {str(e)}") from e
    

def delete_review(self, review_id):
    # Placeholder for logic to delete a review
    pass
