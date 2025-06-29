from flask import Blueprint, request, jsonify, g, session
from marshmallow import ValidationError
from domain.exceptions import InvalidQueryException, PlaceNotFoundException, ExternalServiceException
from application.use_cases.find_places import find_places
from application.services.jwt_service import JWTService
from adapters.web.error_handlers import handle_validation_error
from adapters.web.auth_utils import jwt_required
from infrastructure.db.repositories.user_repository import UserRepository as user_repository
from infrastructure.db.db import SessionLocal
import os, json
from werkzeug.utils import secure_filename
from dataclasses import asdict

jwt_service = JWTService(
    secret_key=os.getenv("JWT_SECRET_KEY"),
    expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", 60))
)
user_repository_factory = lambda: user_repository(SessionLocal())

# Define the blueprint factory function
def create_api_blueprint(find_places_use_case, jwt_required_decorator):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    # --- Search Places Endpoint ---
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
    @jwt_required_decorator
    def get_user_profile():
        # The jwt_required_decorator adds the user object to Flask's global 'g' object
        # or returns an error response if authentication fails.
        current_user = g.current_user # Access the user object set by the decorator

        if not current_user:
            return jsonify({"message": "Authentication required"}), 401

        try:
            social_links = json.loads(current_user.social_links) if current_user.social_links else {}
        except Exception:
            social_links = {}

        # Calculate profile completion percentage
        profile_fields = [
            current_user.name,
            current_user.surname,
            current_user.email,
            current_user.location,
            getattr(current_user, 'social_links', None),  # This might be a JSON string
            getattr(current_user, 'bio', None),
            getattr(current_user, 'profile_picture', None),  # Adjust if you have avatar support
        ]
        filled = sum(1 for f in profile_fields if f)
        profile_completion = int((filled / len(profile_fields)) * 100)

        # Calculate stats
        trips = getattr(current_user, "trips", []) or []
        points = sum(getattr(trip, "points", 0) for trip in trips)

        user_data = {
            "user_id": str(current_user.user_id), # Ensure UUID is converted to string
            "name": current_user.name,
            "surname": current_user.surname,
            "email": current_user.email,
            "location": current_user.location,
            "role": current_user.role,
            "bio": current_user.bio,
            "profile_picture": getattr(current_user, "profile_picture", None),
            "banner_image": getattr(current_user, "banner_image", None),
            "social_links": social_links,
            "bookmarks": [
                {
                    "bookmark_id": str(b.bookmark_id),
                    "user_id": str(b.user_id),
                    "place_id": b.place_id,
                    "name": b.name,
                    "latitude": b.latitude,
                    "longitude": b.longitude
                } for b in current_user.bookmarks
            ],
            "profile_completion": profile_completion,
            "trips_count": len(trips),
            "trips": [asdict(trip) for trip in trips],
            "points": points,
        }

        return jsonify(user_data), 200

    # --- Update User Profile Endpoint ---
    @api_bp.route('/profile', methods=['PUT'])
    @jwt_required_decorator
    def update_profile():
        session = SessionLocal()
        user_repo = user_repository(session)  # Get the user repository instance
        try:
            # Always fetch the user from the session you are about to update!
            user = user_repo.get_by_id(g.current_user.user_id)
            name = request.form.get('name', user.name)
            surname = request.form.get('surname', user.surname)
            email = request.form.get('email', user.email)
            location = request.form.get('location', user.location)
            bio = request.form.get('bio', user.bio)
            social_links = request.form.get('social_links', '{}')

            user.name = name
            user.surname = surname
            user.email = email
            user.location = location
            user.bio = bio
            user.social_links = social_links

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

            # Handle banner image upload
            if 'banner_image' in request.files:
                file = request.files['banner_image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    upload_folder = os.path.join('static', 'uploads')
                    os.makedirs(upload_folder, exist_ok=True)
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    user.banner_image = f'uploads/{filename}'  # Save relative path

            user_repo.update(user)
            session.commit()
            return jsonify({"message": "Profile updated successfully."}), 200
        except Exception as e:
            session.rollback()
            return jsonify({"message": f"Profile update failed: {str(e)}"}), 400
        finally:
            session.close()

    return api_bp