class DomainException(Exception):
    """Base exception for domain errors."""
    pass

class RepositoryException(Exception):
    """"""
    pass

class NotFoundException(Exception):
    """"""
    pass

class ConflictException(Exception):
    """"""
    pass

class EmailAlreadyExistsException(DomainException):
    """Custom exception for registration when email is taken."""
    pass

class InvalidQueryException(DomainException):
    """Raised when a user query cannot be parsed or is invalid."""
    pass

class ExternalServiceException(DomainException):
    """Raised when an external service (like AI or Photon) fails."""
    def __init__(self, message, original_error=None):
        super().__init__(message)
        self.original_error = original_error

class PlaceNotFoundException(DomainException):
    """Raised when a specific place cannot be found."""
    pass