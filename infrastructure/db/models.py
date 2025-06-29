import uuid, json
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from infrastructure.db.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True) 
    password_hash = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)
    bio = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    banner_image = Column(String, nullable=True)
    social_links = Column(Text, nullable=True) 

    # Stats
    points = Column(Integer, default=0)

    # Relationships
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="user")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    bookmark_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    place_id = Column(String)
    name = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    user = relationship("User", back_populates="bookmarks")

    # Add a unique constraint to prevent duplicate bookmarks for the same user and place
    __table_args__ = (UniqueConstraint('user_id', 'place_id', name='_user_place_uc'),)

class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    title = Column(String)
    start_date = Column(String)
    image_url = Column(String)
    points = Column(Integer, default=0)
    user = relationship("User", back_populates="trips")