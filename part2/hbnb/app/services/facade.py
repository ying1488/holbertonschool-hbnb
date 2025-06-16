import uuid
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity

class InvalidPlaceDataError(Exception):
    """Raised when place data is invalid."""

class PlaceNotFoundError(Exception):
    """Raised when a place with the given ID is not found."""

class InvalidPlaceUpdateError(Exception):

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
    
    def updae_user_email(self, user_id, email):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.email = email
        self.user_repo.save(user_id, user)
        return {"message": "User email updated successfully"}

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

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
