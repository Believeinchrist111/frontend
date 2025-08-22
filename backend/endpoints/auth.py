from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import BackgroundTasks
import httpx
from fastapi import Request
import os
from urllib.parse import urlencode


from database import models
from database import schemas
from utility import utils
from utility import oauth2


router = APIRouter(
    tags=["auth"]
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='sign-in')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#store the basic info about the user but mark as unverified
@router.post("/sign-up")
def signup_step1(data: schemas.SignUpStep1, db: Session = Depends(get_db)):
    # check if email exists
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        date_of_birth=data.date_of_birth,
        is_verified=false
    )
    db.add(user)
    db.commit()
    db.refresh(user) # at this stage user is unverified

    code = oauth2.create_verification_entry(db, new_user.user_id) # generates verification code

    if code is None:
        return {"message": "verification code creation failed"}

    background_tasks.add_task(oauth2.send_verification_code, new_user.email, code) # will check for errors



# Step 2: Verify Email
@router.post("/verify-email")
def verify_email(request: schemas.VerifyEmailCode, db: Session = Depends(db_dependency)):

    # Look up the user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # lookup verification code
    verification = (
        db.query(schemas.EmailVerification)
        .filter_by(user_id=user.id, code=request.code, is_used=False)
        .first()
    )

    if not verification:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    if verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code expired")

    user.is_verified = True
    verification.is_used = True
    db.commit()

    return {"message": "Email successfully verified"} # should we ?


# Step 3: Set Password
@router.post("/set-password")
def set_password(data: schemas.SetPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")

    user.password_hash = f"hashed({data.password})"  # Replace with real hash
    db.commit()

    return {"message": "Password set successfully."}


# Step 4: Pick Username
@router.post("/set-username")
def set_username(data: schemas.SetUsername, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=400, detail="Password must be set first")

    existing = db.query(models.User).filter(models.User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user.username = data.username
    db.commit()

    return {"message": "Username set successfully. Account ready to use."}



# Endpoint for signing in or logging into an account
@router.post("/sign-in")
async def login_for_access_token(
    db: Session = Depends(get_db),
    user_cred: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.username == user_cred.username
        )
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password")

    access_token = oauth2.create_access_token(
        data={'user_id': user.id},
    )

    print('the token in the sign in endpoint')
    print(access_token)
    print('the token in the sign in endpoint')

    response = JSONResponse(content={
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    })

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age= 30 * 60,
    )
    return response

@router.get("/login/google")
async def login_google():
    client_id = "some_id"
    redirect_uri = "http://localhost:8000/auth/google/callback"
    scope = "openid email profile"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    }

    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

    #print("Redirecting to:", google_auth_url)  # debug log
    return RedirectResponse(url=google_auth_url)


@router.get("/auth/google/callback")
async def google_callback(
            request: Request,
            code: str,
            db: Session = Depends(get_db)
):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": "some id",
        "client_secret": "some secret",
        "redirect_uri": "http://localhost:8000/auth/google/callback",
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        tokens = token_response.json()

    # Decode ID token to extract user info
    userinfo_url = "https://openidconnect.googleapis.com/v1/userinfo"
    async with httpx.AsyncClient() as client:
        userinfo_response = await client.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        userinfo = userinfo_response.json()

        access_token = oauth2.create_access_token(
        data={'user_id': userinfo["sub"]},
    )

    user = db.query(models.Google_user).filter(models.Google_user.google_sub == userinfo["sub"]).first()

    if not user:
        # Check if user exists by email (link accounts)
        user = db.query(models.Google_user).filter(models.Google_user.email == userinfo["email"]).first()
        if user:
            user.google_sub = userinfo["sub"]
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please sign up first")
            # Create new google user
            #user = models.Google_user(
            #    google_sub=userinfo["sub"],
            #    email=userinfo["email"],
            #    first_name=userinfo.get("given_name"),
            #    last_name=userinfo.get("family_name"),
            #    picture=userinfo.get("picture"),
            #    is_verified = userinfo.get("email_verified"),
            #)
            #db.add(user)
            #db.commit()
            #db.refresh(user)

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # this frontend endpoint shuld be change to /home imo
    response = RedirectResponse(url="http://localhost:3000/")

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age= 30, # none for now
    )

    return response


@router.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_bearer)):
    print("the token in the verify token endpoint")
    print(token)
    print("the token in the verify token endpoint")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = oauth2.verify_access_token(token, credentials_exception)
    return {"user_id": token_data.id}




@router.get("/login", response_model = schemas.UserResponse)
async def read_user(current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    return current_user


# @router.get("/users/me/", response_model=schemas.UserCreate)
# async def read_users_me(current_user: schemas.UserCreate = Depends(oauth2.get_current_user)):
#     return current_user


