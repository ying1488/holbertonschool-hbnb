from flask_restx import Namespace, Resource, fields, abort
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the models for related entities
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        wanted_keys_list = ['text', 'rating', 'user_id', 'place_id']

        # Check that required attributes are present
        if not all(name in review_data for name in wanted_keys_list):
            return {'error': "Invalid input data - required attributes missing"}, 400

        # Check that user exists
        user = facade.get_user(str(review_data.get('user_id')))
        if not user:
            return {'error': "Invalid input data - user does not exist"}, 400

        # Check that place exists
        place = facade.get_place(str(review_data.get('place_id')))
        if not place:
            return {'error': "Invalid input data - place does not exist"}, 400

        # Finally, create the review
        new_review = None
        try:
            new_review = facade.create_review(review_data)
        except ValueError as error:
            return {'error': f"Setter validation failure: {error}"}, 400

        return {'id': str(new_review.id), 'message': 'Review created successfully'}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        output = []

        for review in all_reviews:  # <-- Fixed here: iterate directly over the list
            output.append({
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating
            })
        return output, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        output = {
            'id': str(review.id),
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }
        return output, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        wanted_keys_list = ['text', 'rating', 'user_id', 'place_id']

        # Check that required attributes are present
        if not all(name in review_data for name in wanted_keys_list):
            return {'error': "Invalid input data - required attributes missing"}, 400

        review = facade.get_review(review_id)
        if review:
            try:
                facade.update_review(review_id, review_data)
            except ValueError as error:
                return {'error': f"Setter validation failure: {error}"}, 400

            return {'message': 'Review updated successfully'}, 200
        else:
            return {'error': 'Review not found'}, 404

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            success = facade.delete_review(review_id)
            if not success:
                return {'error': 'Review not found'}, 404
        except ValueError:
            return {'error': "Review not found"}, 404
        return {'message': "Review deleted successfully"}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        output = []

        for review in reviews:  # <-- Fixed here: iterate and accumulate all reviews
            output.append({
                'id': str(review.id),
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
            })
        return output, 200
