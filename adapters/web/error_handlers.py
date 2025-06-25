from flask import jsonify
from marshmallow import ValidationError # For handling Marshmallow validation errors
from domain.exceptions import DomainException, InvalidQueryException, ExternalServiceException, PlaceNotFoundException
from adapters.web.rest.schemas import ErrorSchema # Assuming you have an ErrorSchema

error_schema = ErrorSchema()

def handle_validation_error(err: ValidationError):
    """Handle Marshmallow validation errors."""
    response = error_schema.dump({"message": err.messages})
    return jsonify(response), 400 # Bad Request

def handle_invalid_query_exception(err: InvalidQueryException):
    """Handle domain-specific invalid query errors."""
    response = error_schema.dump({"message": str(err)})
    return jsonify(response), 400 # Bad Request

def handle_place_not_found_exception(err: PlaceNotFoundException):
    """Handle domain-specific place not found errors."""
    response = error_schema.dump({"message": str(err)})
    return jsonify(response), 404 # Not Found

def handle_external_service_exception(err: ExternalServiceException):
    """Handle errors from external services."""
    # Log the original error for debugging
    print(f"External Service Error: {err.original_error}")
    response = error_schema.dump({"message": str(err)})
    return jsonify(response), 503 # Service Unavailable or 500 Internal Server Error

def handle_domain_exception(err: DomainException):
    """Handle generic domain errors."""
    response = error_schema.dump({"message": str(err)})
    return jsonify(response), 400 # Bad Request (or 500 depending on the error)

def handle_exception(e):
    """Handle all other uncaught exceptions."""
    # Log the unexpected error
    print(f"An unexpected error occurred: {e}")
    response = error_schema.dump({"message": "An unexpected error occurred."})
    return jsonify(response), 500 # Internal Server Error