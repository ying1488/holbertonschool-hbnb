from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from app import config
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    bcrypt.init_app(app)
    db.init_app(app)

    # Set up the REST API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    
    # Register the places namespace
    api.add_namespace(review_ns, path='/api/v1/reviews')
    
    return app
