from pydantic import BaseModel, EmailStr, conint, ConfigDict, Field, constr, model_validator
from datetime import datetime, date
from typing import Annotated, Optional, List
from pydantic_extra_types.phone_numbers import PhoneNumber
from fastapi import Form



# This is a three step process for signup
# base sign up page
# verification code sending
# username and password setting
# for signup, we will need a lof info
class UserCreate(BaseModel):
   firstname: Annotated[
   str,
   Field(
       min_length=3,
       max_length=30,
       pattern=r'^[a-zA-Z0-9_]+$',
       strip_whitespace=True
   )
]
   lastname: Annotated[
   str,
   Field(
       min_length=3,
       max_length=30,
       pattern=r'^[a-zA-Z0-9_]+$',
       strip_whitespace=True
   )
]
   email: EmailStr
#    username: Annotated[
#        str,
#        Field(
#            min_length=3,
#            max_length=30,
#            pattern=r'^[a-zA-Z0-9_]+$',
#            strip_whitespace=True
#        )
#    ]
#    phone_number: PhoneNumber
   date_of_birth: date
   password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class SendCodeRequest(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str






# /////////////////////////////////////////////////////////////////



# This is the request model
# the form in which posts are created


# This is the resonse model for a post
# when you are creating a post, the user only cares about their input.
# when it is being displayed, that's when other additional stuff are displayed
# like the time it was created etc.



# Post schemas for media
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
    
class PostCreate(PostBase):
    media_url: Optional[str] = None
    media_items: Optional[List[MediaItem]] = None

    @model_validator(mode="after")
    def content_or_media_required(self) -> "PostCreate":
        if not self.content and not self.media_url and not self.media_items:
            raise ValueError("Post must have at least content or media.")
        return self
        
    
class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    dateOfbirth: date

    model_config = ConfigDict(from_attributes=True)
    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    media_items: List[MediaItem]
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    class Config:
        from_attributes = True



# ////////////////////////////////////////////////////////////

# so for a message request model
# this is the format we have when we are sending a message to someone
# in whoever's DM that we are in, that will be the receiver's id ( and that's compulsory )
# and then we can send either a text or media

# we treat it as a base class
class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int
    content: Optional[str] = None
    reply_to_message_id: Optional[int] = None
    media_id: Optional[int] = None

class MessageCreate(MessageBase):
    pass

# what will be displayed
# when we type a message based on messagecreate model
# this is what will be displayed with extra implicit details
class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)






