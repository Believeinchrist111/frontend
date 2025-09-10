from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette import status
from database.database import SessionLocal, get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import BackgroundTasks
from datetime import datetime, timedelta, timezone
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

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='sign-in')


# Endpoint for signing in or logging into an account
@router.post("/sign-in")
async def login_for_access_token(
    db: Session = Depends(get_db),
    user_cred: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(models.User).filter(
        or_(
            models.User.email == user_cred.username,
            models.User.firstname == user_cred.username
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

    response = JSONResponse(
        content={
        "message": "Login successful",
        # "access_token": access_token,
        "token_type": "bearer"
    })

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age= 30 * 60,
        # domain="localhost"  
    )
    return response


# end point for signin verification token
@router.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_bearer)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = oauth2.verify_access_token(token, credentials_exception)
    return





# //////////////////////////////////////////////////////////////////

# loging in with google
@router.get("/login/google")
async def login_google():
    client_id = "some id"
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


# per research,
# sign up with google will verify user from google first
# after verifying you, if it checks that you already have an account
# in the system, it logs you in directly
# if you don't have account yet, it creates one for you and logs you in
# no striking/strict difference between sign in and sign up with google

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

    if "access_token" not in tokens:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {tokens}")

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
            # automatically treat is as a sign up
            # Create new google user
            user = models.Google_user(
                google_sub=userinfo["sub"],
                email=userinfo["email"],
                first_name=userinfo.get("given_name"),
                last_name=userinfo.get("family_name"),
                picture=userinfo.get("picture"),
                is_verified = userinfo.get("email_verified"),
            )
            db.add(user)
            db.commit()
            db.refresh(user)

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

