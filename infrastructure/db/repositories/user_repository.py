from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
# Import your domain models
from domain.models.user import User as DomainUser
from domain.models.bookmark import Bookmark as DomainBookmark
from domain.models.trip import Trip as DomainTrip
# Import your DB models
from infrastructure.db.models import User as DBUser # Import SQLAlchemy model
from infrastructure.db.models import Bookmark as DBBookmark # Import Bookmark DB model
# Import your exceptions
from domain.exceptions import RepositoryException, NotFoundException, ConflictException # Ensure all necessary exceptions are imported
from typing import List, Optional, Union
import uuid, json

class UserRepository: # This is your existing class
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain_user(self, db_user: Optional[DBUser]) -> Optional[DomainUser]:
        """Converts a SQLAlchemy DBUser model to a Domain User model."""
        if db_user is None:
            return None

        # Convert DB Bookmark models to Domain Bookmark models
        # Ensure db_user.bookmarks is accessed - SQLAlchemy loads this due to relationship
        domain_trips = [
            DomainTrip(
                trip_id=str(db_trip.trip_id),
                user_id=str(db_trip.user_id),
                title=db_trip.title,
                start_date=db_trip.start_date,
                image_url=db_trip.image_url,
                points=db_trip.points
            ) for db_trip in db_user.trips
        ]
        domain_bookmarks = [
            DomainBookmark(
                bookmark_id=str(db_bookmark.bookmark_id),
                user_id=str(db_bookmark.user_id),
                place_id=db_bookmark.place_id,
                name=db_bookmark.name,
                latitude=db_bookmark.latitude,
                longitude=db_bookmark.longitude
            ) for db_bookmark in db_user.bookmarks # Access the loaded bookmarks relationship
        ]

        # Ensure all fields expected by the DomainUser dataclass are mapped
        return DomainUser(
            user_id=str(db_user.user_id),
            name=db_user.name,
            surname=db_user.surname,
            email=db_user.email,
            location=db_user.location, 
            password_hash=db_user.password_hash,
            role=db_user.role,
            bio=db_user.bio,
            profile_picture=db_user.profile_picture,
            banner_image=db_user.banner_image,
            social_links=json.loads(db_user.social_links) if db_user.social_links else {},
            trips=domain_trips,
            bookmarks=domain_bookmarks,
        )

    def _to_db_user(self, domain_user: DomainUser) -> DBUser:
         """Converts a Domain User model to a SQLAlchemy DBUser model."""
         # Ensure all fields expected by the DBUser model are mapped
         # Note: Bookmarks are typically managed via separate add/remove methods
         # or by loading the DBUser and modifying its bookmarks list directly.
         # For this conversion back to DB model, we typically don't include the list.
         db_user = DBUser(
            user_id=uuid.UUID(domain_user.user_id) if isinstance(domain_user.user_id, str) else domain_user.user_id,
            name=domain_user.name,
            surname=domain_user.surname,
            email=domain_user.email,
            location=domain_user.location,
            password_hash=domain_user.password_hash,
            role=domain_user.role,
            bio=domain_user.bio,
            profile_picture=domain_user.profile_picture,
            banner_image=domain_user.banner_image,
            social_links=json.dumps(domain_user.social_links) if domain_user.social_links else None,
         )
         # print(f"[_to_db_user] Domain User ID: {domain_user.user_id}") # Debug print
         # print(f"[_to_db_user] DBUser ID after mapping: {db_user.user_id}") # Debug print
         return db_user

    def get_by_id(self, user_id: Union[uuid.UUID]) -> Optional[DomainUser]:
        """Get a user by their ID."""
        if isinstance(user_id, str):
            user_id = uuid.UUID(user_id)
        try:
            # SQLAlchemy automatically loads relationships defined with relationship()
            # when you query the parent object.
            db_user = self.db_session.query(DBUser).filter(DBUser.user_id == user_id).first()
            return self._to_domain_user(db_user)
        except Exception as e:
            raise RepositoryException(f"Error getting user by ID {user_id}: {e}") from e

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        """Get a user by their email address."""
        try:
            # SQLAlchemy automatically loads relationships defined with relationship()
            db_user = self.db_session.query(DBUser).filter(DBUser.email == email).first()
            return self._to_domain_user(db_user)
        except Exception as e:
            raise RepositoryException(f"Error getting user by email {email}: {e}") from e

    def create(self, user: DomainUser) -> DomainUser:
        """Create a new user from a DomainUser model."""
        # print(f"[UserRepository.create] Domain User object received: {user}") # Debug print
        # print(f"[UserRepository.create] Domain User ID before mapping: {user.user_id}") # Debug print

        try:
            db_user = self._to_db_user(user)

            # print(f"[UserRepository.create] DBUser object before add: {db_user}") # Debug print
            # print(f"[UserRepository.create] DBUser ID before add: {db_user.user_id}") # Debug print

            self.db_session.add(db_user)

            # print("[UserRepository.create] DBUser added to session. Committing...") # Debug print
            self.db_session.commit()
            # print("[UserRepository.create] Commit successful. Refreshing...") # Debug print

            self.db_session.refresh(db_user) # Refresh to get the generated ID (though it should already have one)
            # print(f"[UserRepository.create] DBUser ID after refresh: {db_user.user_id}") # Debug print

            return self._to_domain_user(db_user) # Return the created DomainUser with ID
        except IntegrityError as e:
            self.db_session.rollback()
            # Check for specific integrity errors (e.g., unique constraint violation)
            if "UNIQUE constraint failed: users.email" in str(e):
                 raise ConflictException(f"User with email {user.email} already exists.") from e
            raise RepositoryException(f"Database integrity error creating user: {e}") from e
        except Exception as e:
            self.db_session.rollback()
            raise RepositoryException(f"Error creating user: {e}") from e

    def update(self, user: DomainUser) -> DomainUser:
        """Update an existing user in the database."""
        if isinstance(user.user_id, str):
            user.user_id = uuid.UUID(user.user_id)
        try:
            db_user = self.db_session.query(DBUser).filter(DBUser.user_id == user.user_id).first()
            if not db_user:
                raise NotFoundException(f"User with ID {user.user_id} not found.")
            
            print(f"Updating location: {db_user.location} -> {user.location}")

            # Update fields
            db_user.name = user.name
            db_user.surname = user.surname
            db_user.email = user.email
            db_user.location = user.location
            # Add other fields as needed, e.g., bio, avatar_url
            if hasattr(user, 'bio'):
                db_user.bio = user.bio
            if hasattr(user, 'profile_picture'):
                db_user.profile_picture = user.profile_picture
            if hasattr(user, 'banner_image'):
                db_user.banner_image = user.banner_image
            if hasattr(user, 'social_links'):
                db_user.social_links = json.dumps(user.social_links) if user.social_links else None

            self.db_session.commit()
            self.db_session.refresh(db_user)
            return self._to_domain_user(db_user)
        except IntegrityError as e:
            self.db_session.rollback()
            if "UNIQUE constraint failed: users.email" in str(e):
                raise ConflictException(f"User with email {user.email} already exists.") from e
            raise RepositoryException(f"Database integrity error updating user: {e}") from e
        except Exception as e:
            self.db_session.rollback()
            raise RepositoryException(f"Error updating user: {e}") from e

    # --- Add methods for managing bookmarks ---
    def add_bookmark(self, user_id: uuid.UUID, place_id: str, name: str, latitude: float, longitude: float) -> DomainBookmark:
        """Adds a new bookmark for a user."""
        try:
            # Check if bookmark already exists for this user and place
            existing_bookmark = self.db_session.query(DBBookmark).filter_by(user_id=user_id, place_id=place_id).first()
            if existing_bookmark:
                # Raise ConflictException if it already exists
                raise ConflictException(f"Place {place_id} is already bookmarked by user {user_id}.")

            db_bookmark = DBBookmark(
                user_id=user_id,
                place_id=place_id,
                name=name,
                latitude=latitude,
                longitude=longitude
            )
            self.db_session.add(db_bookmark)
            self.db_session.commit()
            self.db_session.refresh(db_bookmark) # Refresh to get the generated bookmark_id
            return DomainBookmark(
                bookmark_id=db_bookmark.bookmark_id,
                user_id=db_bookmark.user_id,
                place_id=db_bookmark.place_id,
                name=db_bookmark.name,
                latitude=db_bookmark.latitude,
                longitude=db_bookmark.longitude
            )
        except IntegrityError as e:
             self.db_session.rollback()
             # Handle potential unique constraint violation if added
             if "_user_place_uc" in str(e): # Check for the unique constraint name
                  raise ConflictException(f"Place {place_id} is already bookmarked by user {user_id}.") from e
             raise RepositoryException(f"Database integrity error adding bookmark: {e}") from e
        except ConflictException:
             self.db_session.rollback()
             raise # Re-raise the specific exception
        except Exception as e:
            self.db_session.rollback()
            raise RepositoryException(f"Error adding bookmark: {e}") from e

    def remove_bookmark(self, user_id: uuid.UUID, place_id: str) -> None:
        """Removes a bookmark for a user by place ID."""
        try:
            db_bookmark = self.db_session.query(DBBookmark).filter_by(user_id=user_id, place_id=place_id).first()
            if not db_bookmark:
                raise NotFoundException(f"Bookmark for place {place_id} not found for user {user_id}.")
            self.db_session.delete(db_bookmark)
            self.db_session.commit()
        except NotFoundException:
            self.db_session.rollback()
            raise # Re-raise the specific exception
        except Exception as e:
            self.db_session.rollback()
            raise RepositoryException(f"Error removing bookmark: {e}") from e

    def get_bookmarks_by_user_id(self, user_id: uuid.UUID) -> List[DomainBookmark]:
        """Gets all bookmarks for a specific user."""
        try:
            db_bookmarks = self.db_session.query(DBBookmark).filter_by(user_id=user_id).all()
            return [
                 DomainBookmark(
                    bookmark_id=db_bookmark.bookmark_id,
                    user_id=db_bookmark.user_id,
                    place_id=db_bookmark.place_id,
                    name=db_bookmark.name,
                    latitude=db_bookmark.latitude,
                    longitude=db_bookmark.longitude
                ) for db_bookmark in db_bookmarks
            ]
        except Exception as e:
            raise RepositoryException(f"Error getting bookmarks for user {user_id}: {e}") from e

    def is_bookmarked(self, user_id: uuid.UUID, place_id: str) -> bool:
        """Checks if a place is bookmarked by a user."""
        try:
            count = self.db_session.query(DBBookmark).filter_by(user_id=user_id, place_id=place_id).count()
            return count > 0
        except Exception as e:
            raise RepositoryException(f"Error checking if place {place_id} is bookmarked by user {user_id}: {e}") from e