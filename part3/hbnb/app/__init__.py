from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from app import config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    app.config['JWT_SECRET_KEY'] = 'wonderful_secret_key'
    jwt = JWTManager(app)

    bcrypt.init_app(app)
    db.init_app(app)

    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as review_ns

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')

    return app
