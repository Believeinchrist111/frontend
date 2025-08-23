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


# Endpoint for signing up or creating an account
# Email verification endpoints
@router.post("/send-code")
async def send_token(req: schemas.SendCodeRequest, db: db_dependency):
    try:
        Code = oauth2.create_verification_token(req.email)

        # Create a new record
        record = models.EmailVerification(
            firstname=req.firstname,
            lastname=req.lastname,
            email=req.email,
            code=Code,
            verified=False
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # Send verification email
        await oauth2.send_verification_email(req.email, Code)

        return {"msg": "Verification token sent to email"}
    except Exception as e:
        print("ERROR in /send-code:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-code")
async def verify_user_token(req: schemas.VerifyCodeRequest, db: db_dependency):
    # Find user by email
    user = db.query(models.EmailVerification).filter(models.EmailVerification.email == req.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    # This is the correct logic for a simple code
    if user.code != req.code:
        raise HTTPException(status_code=400, detail="Invalid code")


    # Mark user as verified
    user.verified = True
    db.commit()
    db.refresh(user)

    # Send confirmation email
    await oauth2.send_confirmation_email(req.email)

    return {"msg": "Email successfully verified"}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserCreate, db: db_dependency):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(user) # at this stage user is unverified


# //////////////////////////////////////////////////////////////////////


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



# /////////////////////////////////////////////////////////////////////

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


