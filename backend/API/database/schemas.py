from pydantic import BaseModel, EmailStr, conint, ConfigDict, Field, constr
from datetime import datetime, date
from typing import Annotated
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
