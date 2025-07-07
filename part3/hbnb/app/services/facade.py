import uuid
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository


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
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
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
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required")
        amenity = Amenity(name=name)
        self.amenity_repo.save(amenity)  # saves the object
        return amenity.to_dict() 

    def get_all_amenities(self):
        amenities = self.amenity_repo.all()
        return [a.to_dict() for a in amenities]  # <-- convert all to dicts

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return amenity.to_dict()

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
        try:
            owner_id = place_data.pop('owner_id')
            # Fix if owner_id is tuple or list
            if isinstance(owner_id, (tuple, list)):
                owner_id = owner_id[0]

            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError(f"Owner with ID '{owner_id}' not found")

            amenity_ids = place_data.pop('amenities', [])
            place_data.pop('reviews', None)
            new_place = Place(owner=owner, **place_data)
            new_place.owner_r = owner  # make sure this matches your relationship name

            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    new_place.amenities_r.append(amenity)

            self.place_repo.add(new_place)
            return new_place.to_dict()

        except ValueError as e:
            raise InvalidPlaceDataError(f"Invalid data: {str(e)}") from e
    
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.to_dict()

    def get_all_places(self):
        return [place.to_dict() for place in self.place_repo.all()]


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
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.all()

    def get_reviews_by_place(self, place_id):
        #Placeholder for retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        # Check if review is in the reviews
        review = self.get_review(review_id)
        if not review:
            return False
        # Remove review from place's reviews list
        if review.place and hasattr(review.place, 'reviews'):
            if review in review.place.reviews:
                review.place.reviews.remove(review)
    
        # Delete from repository
        self.review_repo.delete(review_id)
        return True 
