from flask_restx import Api
from .v1.amenities import api as amenities_ns

api = Api()

def initialize_app(app):
    api.init_app(app)
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
