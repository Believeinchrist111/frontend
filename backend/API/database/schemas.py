from pydantic import BaseModel, EmailStr, conint, ConfigDict
from datetime import datetime

# let's receive login request as JSON for now
# can change to forms
class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
