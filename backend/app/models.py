# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum,Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base  # ✅ use the Base from database.py

# Enum for user roles
class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

# --------------------------
# User Table
# --------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)


# --------------------------
# Reddit Post Table
# --------------------------
class RedditPost(Base):
    __tablename__ = "reddit_posts"

    id = Column(Integer, primary_key=True, index=True)
    subreddit = Column(String)
    title = Column(String)
    text = Column(Text)
    score = Column(Integer)
    url = Column(String)
    sentiment = Column(String)
    emotion = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# --------------------------
# Analysis Result Table (optional, uncomment if needed later)
# --------------------------
# class AnalysisResult(Base):
#     __tablename__ = "analysis_results"
#
#     id = Column(Integer, primary_key=True, index=True)
#     post_id = Column(Integer, ForeignKey("reddit_posts.id"), nullable=False)
#     sentiment = Column(String(20))  # Positive, Negative, Neutral
#     keywords = Column(Text)  # Comma-separated keywords
#     analyzed_at = Column(DateTime, default=datetime.utcnow)
#
#     post = relationship("RedditPost", backref="analysis")
