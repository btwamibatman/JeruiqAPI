import uuid, json
from sqlalchemy import Column, String, ForeignKey, Float, UniqueConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from infrastructure.db.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)
    bio = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)  # Store profile picture as URL or path
    social_links = Column(Text, nullable=True)  # Store as JSON or text for social media links

    # Define the relationship to Bookmarks
    # 'bookmarks' will be a list of Bookmark objects associated with this user
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    # Foreign key to the users table
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    # Use UUID type for primary key
    bookmark_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    # Fields for the bookmarked place
    place_id = Column(String, nullable=False) # Unique ID from the external service or internal
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Define the relationship back to the User
    user = relationship("User", back_populates="bookmarks")

    # Add a unique constraint to prevent duplicate bookmarks for the same user and place
    __table_args__ = (UniqueConstraint('user_id', 'place_id', name='_user_place_uc'),) # Add if needed