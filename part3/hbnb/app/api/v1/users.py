from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token
from flask import make_response
from datetime import timedelta
from flask import request
from app import bcrypt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """Get a list of all users"""
        users = facade.get_all_users()
        return users, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/email/<string:email>')
class UserEmailResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, email):
        """Get user details by email"""
        user = facade.get_user_by_email(email)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/<user_id>/update_name')
class UserUpdateNameResource(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User name updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user's first and last name"""
        user_data = api.payload
        updated_user = facade.update_user_name(user_id, user_data.get('first_name'), user_data.get('last_name'))
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User name updated successfully'}, 200

@api.route('/<user_id>/update_email')
class UserUpdateEmailResource(Resource):
    @api.expect(fields.String(required=True, description='New email for the user'))
    @api.response(200, 'User email updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user's email"""
        new_email = api.payload
        updated_user = facade.update_user_email(user_id, new_email)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User email updated successfully'}, 200
    
@api.route('/<user_id>/update')
class UserUpdateResource(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User updated successfully', 'user': {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }}, 200

@api.route('/login')
class UserLoginResource(Resource):
    @api.expect(api.model('Login', {
        'email': fields.String(required=True, description='Email of the user'),
        'password': fields.String(required=True, description='Password of the user')
    }), validate=True)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = facade.get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password, password):
            return {'error': 'Invalid email or password'}, 401

        token = create_access_token(identity=user.id)

        response_data = {
            'message': 'Login successful',
            'token': token,
            'user_id': str(user.id)
        }

        response = make_response(response_data)
        response.set_cookie(
            'token',
            token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=60 * 60
        )
        return response
