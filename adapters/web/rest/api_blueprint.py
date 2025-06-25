from flask import Blueprint, request, jsonify, g # Import g to access g.current_user
from marshmallow import ValidationError
from .schemas import FindPlacesRequestSchema, PlaceSchema, ErrorSchema
# Import the decorator factory type hint (optional)
from adapters.web.auth_utils import jwt_required

# Define a function that creates the blueprint and accepts dependencies
# Accept the jwt_required_decorator instance
def create_api_blueprint(find_places_use_case, jwt_required_decorator: jwt_required):
    api_blueprint = Blueprint('api', __name__)

    # Instantiate schemas
    find_places_request_schema = FindPlacesRequestSchema()
    place_schema = PlaceSchema()
    error_schema = ErrorSchema()

    # Apply the decorator to the route that requires authentication
    @api_blueprint.route("/find_places", methods=["POST"])
    @jwt_required_decorator # Apply the decorator here
    def find_places_endpoint():
        """
        POST /find_places
        Requires JWT Authentication.
        Request JSON: { "query": "Show me cafes with rating above 4.5" }
        Response: List of places matching the query
        """
        # Access the authenticated user from g if needed
        current_user = g.current_user
        print(f"Authenticated user accessing /find_places: {current_user.email} (ID: {current_user.id})")

        json_data = request.get_json()

        # 1. Input Validation using Schema
        try:
            data = find_places_request_schema.load(json_data)
            user_text = data['query']
        except ValidationError as err:
            # Note: Validation errors should ideally be caught before authentication,
            # but applying the decorator first is simpler. If validation fails
            # after auth, it's still a 400.
            return jsonify(error_schema.dump({"message": err.messages})), 400

        # 2. Call the injected use case
        try:
            # You could potentially pass the current_user to the use case
            # if the use case logic depends on the authenticated user.
            places = find_places_use_case(user_text)

            # 3. Output Serialization using Schema
            result = place_schema.dump(places, many=True)

            return jsonify(result), 200

        except Exception as e:
            print(f"Error in find_places_endpoint: {e}")
            return jsonify(error_schema.dump({"message": "An internal server error occurred."})), 500

    return api_blueprint