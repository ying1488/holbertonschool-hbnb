from app.models.base_model import BaseModel


class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place):
        self.places.append(place)
        self.save()

    def __str__(self):
        """Return a string representation of the User instance."""
        return (f"User(first_name={self.first_name}, last_name={self.last_name}, "
                f"email={self.email}, is_admin={self.is_admin}, "
                f"id={self.id}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def update_name(self, first_name=None, last_name=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        self.save()

    def update_email(self, email):
        self.email = email
        self.save()
    
    def delete_place(self, place):
        if place in self.places:
            self.places.remove(place)
            self.save()
        else:
            print("Place not found in user's places.")

    def delete_account(self):
        for place in self.places:
            place.delete()
        self.places.clear()
        self.first_name = None
        self.last_name = None
        self.email = None
        self.is_admin = False
        self.id = None
        self.created_at = None
        self.updated_at = None
    
    def update(self, data):
        return super().update(data)

    


