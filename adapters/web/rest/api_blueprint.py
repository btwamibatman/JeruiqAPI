from flask import Blueprint, request, jsonify, g
from marshmallow import ValidationError
from domain.exceptions import InvalidQueryException, PlaceNotFoundException, ExternalServiceException
from adapters.web.error_handlers import handle_validation_error # Import the handler
from application.use_cases.find_places import find_places # Assuming this is the correct import
from adapters.web.auth_utils import jwt_required # Import the decorator factory
from infrastructure.db.repositories.user_repository import UserRepository as user_repository # Import the user repository
from infrastructure.db.db import SessionLocal # Import the session factory
import uuid, os, json
from werkzeug.utils import secure_filename

# Define the blueprint factory function
def create_api_blueprint(find_places_use_case, jwt_required_decorator):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route('/search', methods=['GET'])
    def search_places():
        query = request.args.get('q')
        if not query:
            # Use the imported handler or raise a specific exception
            # return handle_validation_error(ValidationError({"q": ["Missing data for required field."]}))
             raise ValidationError({"q": ["Missing data for required field."]})

        try:
            # The find_places_use_case is a lambda/function injected from app.py
            # It should handle the logic of calling the domain service and infrastructure client
            places = find_places_use_case(query)
            # Assuming places is a list of dictionaries or objects that are jsonify-able
            return jsonify(places)
        except InvalidQueryException as e:
             # Use the imported handler or raise the exception
             # return handle_invalid_query_exception(e)
             raise e
        except PlaceNotFoundException as e:
             # Use the imported handler or raise the exception
             # return handle_place_not_found_exception(e)
             raise e
        except ExternalServiceException as e:
             # Use the imported handler or raise the exception
             # return handle_external_service_exception(e)
             raise e
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred during search: {e}")
            # return jsonify({"error": "An internal error occurred"}), 500
            raise e # Let the app-level handler catch it

    # --- New Endpoint for User Profile ---
    @api_bp.route('/profile', methods=['GET'])
    @jwt_required_decorator # Protect this route
    def get_user_profile():
        # The jwt_required_decorator adds the user object to Flask's global 'g' object
        # or returns an error response if authentication fails.
        current_user = g.current_user # Access the user object set by the decorator

        if not current_user:
            # This case should ideally be handled by the decorator returning 401,
            # but it's a good safeguard.
            return jsonify({"message": "Authentication required"}), 401

        # Prepare the user data to return.
        # Include basic info and potentially a list of bookmarked place names/IDs.

        profile_fields = [
            bool(current_user.name),
            bool(current_user.surname),
            bool(current_user.email),
            bool(getattr(current_user, 'bio', None)),
            bool(getattr(current_user, 'profile_picture', None)),  # Adjust if you have avatar support
        ]
        profile_completion = int(100 * sum(profile_fields) / len(profile_fields))

        user_data = {
            "user_id": str(current_user.user_id), # Ensure UUID is converted to string
            "name": current_user.name,
            "surname": current_user.surname,
            "email": current_user.email,
            "role": current_user.role,
            "bio": current_user.bio,
            "profile_picture": getattr(current_user, "profile_picture", None),
            "social_links": json.loads(current_user.social_links) if current_user.social_links else {},
            "bookmarks": [
                {
                    "bookmark_id": str(b.bookmark_id),
                    "user_id": str(b.user_id),
                    "place_id": b.place_id,
                    "name": b.name,
                    "latitude": b.latitude,
                    "longitude": b.longitude
                } for b in current_user.bookmarks # Access the bookmarks list from the domain model
            ],
            "profile_completion": profile_completion,
            # Add other profile information as needed
        }

        return jsonify(user_data), 200

    # --- Update User Profile Endpoint ---
    @api_bp.route('/profile', methods=['PUT'])
    @jwt_required_decorator
    def update_profile():
        user = g.current_user
        g.db_session = SessionLocal()
        # Use request.form for text fields and request.files for files
        name = request.form.get('name', user.name)
        surname = request.form.get('surname', user.surname)
        email = request.form.get('email', user.email)
        bio = request.form.get('bio', user.bio)
        social_links = request.form.get('social_links', '{}')

        user.name = name
        user.surname = surname
        user.email = email
        user.bio = bio
        user.social_links = social_links  # Store as JSON string

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                user.profile_picture = f'uploads/{filename}'  # Save relative path

        user_repo = user_repository(g.db_session)  # Get the user repository instance
        user_repo.update(user)
        return jsonify({"message": "Profile updated successfully."}), 200

    return api_bp