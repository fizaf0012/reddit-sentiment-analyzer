from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List

# --------------------------
# Role Enum
# --------------------------
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


# --------------------------
# Base User (shared fields)
# --------------------------
class UserBase(BaseModel):
    username: str
    email: EmailStr


# --------------------------
# User Create Schema (request)
# --------------------------
class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user


# --------------------------
# User Response Schema (response)
# --------------------------
class UserResponse(UserBase):
    id: int
    role: RoleEnum

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


# --------------------------
# Login Schema
# --------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
class RedditPostBase(BaseModel):
    subreddit: str
    title: str
    score: int
    url: str

class RedditPostResponse(RedditPostBase):
    id: int

    class Config:
        from_attributes = True

class SentimentResponse(BaseModel):
    text: str
    emotion: str
    sentiment: str
    confidence: float

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]