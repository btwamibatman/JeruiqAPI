from flask import Blueprint, request, jsonify, make_response
from marshmallow import ValidationError
from .schemas import (
    RegisterRequestSchema,
    LoginRequestSchema,
    LoginResponseSchema,
    UserResponseSchema,
    ErrorSchema
)
# Import use cases and exceptions
from application.use_cases.register_user import register_user, EmailAlreadyExistsException
from application.use_cases.login_user import login_user, InvalidCredentialsException
from domain.exceptions import DomainException # Catch generic domain errors

# Define a function that creates the blueprint and accepts dependencies
def create_auth_blueprint(register_user_use_case, login_user_use_case): # Accept use cases as dependencies
    auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth') # Add a URL prefix

    # Instantiate schemas
    register_request_schema = RegisterRequestSchema()
    login_request_schema = LoginRequestSchema()
    login_response_schema = LoginResponseSchema()
    user_response_schema = UserResponseSchema()
    error_schema = ErrorSchema()

    @auth_blueprint.route("/register", methods=["POST"])
    def register():
        """
        POST /auth/register
        Handles user registration.
        """
        json_data = request.get_json()

        # 1. Input Validation using Schema
        try:
            data = register_request_schema.load(json_data)
            # data will contain 'name', 'email', 'password' based on the schema
            name = data['name'] # This will contain the combined name and surname from frontend
            surname = data['surname']
            email = data['email']
            plain_password = data['password']
        except ValidationError as err:
            return jsonify(error_schema.dump({"message": err.messages})), 400

        # 2. Call the injected use case
        try:
            # Pass the extracted data to the use case
            new_user = register_user_use_case(name=name, surname=surname, email=email, plain_password=plain_password)

            # 3. Output Serialization using Schema
            result = user_response_schema.dump(new_user)

            return jsonify(result), 201 # Created

        except EmailAlreadyExistsException as e:
             # Specific handling for domain exceptions
             return jsonify(error_schema.dump({"message": str(e)})), 409 # Conflict
        except DomainException as e:
             # Catch other domain exceptions
             return jsonify(error_schema.dump({"message": str(e)})), 400 # Bad Request or other appropriate code
        except Exception as e:
            print(f"Error during registration: {e}")
            return jsonify(error_schema.dump({"message": "An internal server error occurred during registration."})), 500

    @auth_blueprint.route("/login", methods=["POST"])
    def login():
        """
        POST /auth/login
        Handles user login and returns a JWT token.
        """
        json_data = request.get_json()

        # 1. Input Validation using Schema
        try:
            data = login_request_schema.load(json_data)
            email = data['email']
            plain_password = data['password']
        except ValidationError as err:
            return jsonify(error_schema.dump({"message": err.messages})), 400

        # 2. Call the injected use case
        try:
            # Pass the extracted data to the use case
            token = login_user_use_case(email=email, plain_password=plain_password)

            # 3. Output Serialization using Schema
            result = login_response_schema.dump({"token": token})

            return jsonify(result), 200 # OK

        except InvalidCredentialsException as e:
             # Specific handling for domain exceptions
             return jsonify(error_schema.dump({"message": str(e)})), 401 # Unauthorized
        except DomainException as e:
             # Catch other domain exceptions
             return jsonify(error_schema.dump({"message": str(e)})), 400 # Bad Request or other appropriate code
        except Exception as e:
            print(f"Error during login: {e}")
            return jsonify(error_schema.dump({"message": "An internal server error occurred during login."})), 500

    # You might add a /logout route here later

    return auth_blueprint