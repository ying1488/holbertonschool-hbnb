from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.base_model import BaseModel

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
