import bcrypt

class PasswordHasher:
    """Handles password hashing and verification."""

    def hash_password(self, password: str) -> str:
        """Hashes a plain text password."""
        # bcrypt generates a salt automatically
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a hashed password."""
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            # Handle cases where the hashed password might be invalid
            return False