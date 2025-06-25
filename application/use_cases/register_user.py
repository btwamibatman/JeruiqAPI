from domain.models.user import User # Ensure this imports the dataclass User
from infrastructure.db.repositories.user_repository import UserRepository
from application.services.password_hasher import PasswordHasher
from domain.exceptions import EmailAlreadyExistsException

def register_user(name: str, surname: str, email: str, plain_password: str, user_repository: UserRepository, password_hasher: PasswordHasher) -> User:
    """
    Registers a new user.

    Args:
        name: The user's first name.
        surname: The user's surname.
        email: The user's email address.
        plain_password: The user's plain password.
        user_repository: The repository for user data.
        password_hasher: The service for hashing passwords.

    Returns:
        The newly created User domain model.

    Raises:
        EmailAlreadyExistsException: If a user with the given email already exists.
    """
    # Check if user already exists
    existing_user = user_repository.get_by_email(email)
    if existing_user:
        raise EmailAlreadyExistsException(f"User with email '{email}' already exists.")

    # Hash the password
    hashed_password = password_hasher.hash_password(plain_password)

    # Create the User domain model
    # The user_id should be generated here by the dataclass default_factory
    new_user = User(
        name=name,
        surname=surname,
        email=email,
        password_hash=hashed_password,
        # user_id and role will use their default values from the dataclass definition
    )

    # --- Add these print statements ---
    print(f"[register_user Use Case] Created Domain User object: {new_user}")
    # Check if the attribute exists before trying to print its value
    if hasattr(new_user, 'user_id'):
        print(f"[register_user Use Case] Domain User ID after creation: {new_user.user_id}")
    else:
        print("[register_user Use Case] Domain User object does NOT have 'user_id' attribute.")
    # --- End of print statements ---


    # Save the user to the database
    created_user = user_repository.create(new_user)

    return created_user