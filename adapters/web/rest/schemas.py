from marshmallow import Schema, fields, validate

# Schema for the request body of the /find_places endpoint
class FindPlacesRequestSchema(Schema):
    query = fields.String(required=True, validate=validate.Length(min=1))

# Schema for the Place domain model (for serialization)
class PlaceSchema(Schema):
    name = fields.String(required=True)
    lat = fields.Float(required=True)
    lon = fields.Float(required=True)
    category = fields.String(allow_none=True)
    rating = fields.Float(allow_none=True)
    address = fields.String(allow_none=True)
    source_id = fields.String(allow_none=True)

# Schema for the response body of the /find_places endpoint (list of places)
class FindPlacesResponseSchema(Schema):
    places = fields.List(fields.Nested(PlaceSchema))

# Schema for a generic error response
class ErrorSchema(Schema):
    message = fields.String(required=True)

# Schema for the request body of the /ai/response endpoint
class AIRequestSchema(Schema):
    message = fields.String(required=True, validate=validate.Length(min=1))

# Schema for the response body of the /ai/response endpoint
class AIResponseSchema(Schema):
    message = fields.String(required=True)

class AIQueryRequestSchema(Schema):
    """Schema for validating AI query requests."""
    query = fields.String(required=True, validate=validate.Length(min=1))
    session_id = fields.String(required=False, allow_none=True)

# Schema for the request body of the /register endpoint
class RegisterRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    surname = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True) # Use Email field for validation
    password = fields.String(required=True, validate=validate.Length(min=6)) # Add password strength validation if needed

# Schema for the request body of the /login endpoint
class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

# Schema for a successful login response (returning JWT)
class LoginResponseSchema(Schema):
    token = fields.String(required=True)

# Schema for a successful registration response (returning user info, excluding password hash)
class UserResponseSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    email = fields.Email(required=True)
    role = fields.String(required=True)