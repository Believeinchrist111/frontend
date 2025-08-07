from pydantic import BaseModel, EmailStr, conint, ConfigDict, Field, constr, model_validator
from datetime import datetime, date
from typing import Annotated, Optional, List
from pydantic_extra_types.phone_numbers import PhoneNumber

# let's receive login request as JSON for now
# can change to forms
class LoginRequest(BaseModel):
    username: str
    password: str

# for signup, we will need a ot of info
class UserCreate(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=100)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=100)
    email: EmailStr
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            pattern=r'^[a-zA-Z0-9_]+$',
            strip_whitespace=True
        )
    ]
    phone_number: PhoneNumber
    date_of_birth: date
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

class MediaItem(BaseModel):
    file_url: str
    type: str

    class config:
        from_attributes = True

# base class for a post
class PostBase(BaseModel):
    content: Optional[str] = None
    reply_to_post_id: Optional[int] = None
    repost_of_post_id: Optional[int] = None
    is_repost: bool = False
    # published: bool = True ? do we want to support drafts ?


# can have more than one media or ?
class PostCreate(PostBase):
    media_url: Optional[str] = None
    media_items: Optional[List[MediaItem]] = None

    @model_validator(mode="after")
    def content_or_media_required(self) -> "PostCreate":
        if not self.content and not self.media_url and not self.media_items:
            raise ValueError("Post must have at least content or media.")
        return self

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    media_items: List[MediaItem]
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
