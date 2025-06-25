from flask import Blueprint, request, jsonify, g # Import g to access g.current_user
from marshmallow import ValidationError
from .schemas import AIQueryRequestSchema, AIResponseSchema, ErrorSchema # Import schemas
# Import the decorator factory type hint (optional)
from adapters.web.auth_utils import jwt_required
# Import the ChatSessionManager type hint
from application.services.chat_session_manager import ChatSessionManager

# Define a function that creates the blueprint and accepts dependencies
# Accept the jwt_required_decorator instance
def create_ai_blueprint(session_manager: ChatSessionManager, jwt_required_decorator: jwt_required):
    ai_blueprint = Blueprint('ai', __name__, url_prefix='/ai') # Add a URL prefix

    # Instantiate schemas
    ai_query_request_schema = AIQueryRequestSchema()
    ai_response_schema = AIResponseSchema()
    error_schema = ErrorSchema()

    # Apply the decorator to the route that requires authentication
    @ai_blueprint.route("/response", methods=["POST"])
    @jwt_required_decorator # Apply the decorator here
    def get_ai_response():
        """
        POST /ai/response
        Requires JWT Authentication.
        Handles AI chat interactions.
        """
        # Access the authenticated user from g
        current_user = g.current_user
        print(f"Authenticated user accessing /ai/response: {current_user.email} (ID: {current_user.id})")

        json_data = request.get_json()

        # 1. Input Validation using Schema
        try:
            data = ai_query_request_schema.load(json_data)
            user_query_text = data['query']
            session_id = data.get('session_id') # Get session_id if provided
        except ValidationError as err:
            return jsonify(error_schema.dump({"message": err.messages})), 400

        # 2. Get or create chat session using the session manager
        # Pass the user ID to the session manager
        session = session_manager.get_or_create_session(session_id, user_id=current_user.id)

        # 3. Process the query using the session (which might use domain services/infra clients internally)
        try:
            ai_response_text = session.process_query(user_query_text) # Assuming session object has this method

            # 4. Output Serialization using Schema
            response_data = {
                "response": ai_response_text,
                "session_id": session.id # Return the session ID
            }
            result = ai_response_schema.dump(response_data)

            return jsonify(result), 200

        except Exception as e:
            print(f"Error in get_ai_response endpoint: {e}")
            # You might want more specific error handling based on exceptions from session.process_query
            return jsonify(error_schema.dump({"message": "An internal server error occurred while processing AI query."})), 500

    # You might have other AI-related routes here (e.g., /ai/sessions, /ai/sessions/<id>)

    return ai_blueprint