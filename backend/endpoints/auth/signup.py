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


#store the basic info about the user but mark as unverified
@router.post("/sign-up")
def signup_step1(data: schemas.SignUpStep1, db: Session = Depends(get_db)):
    # check if email exists
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # if a user signs up without verifying himself, store his/her details
    # in the database but mark him not verified
    # if we don't store it here, we are never getting it
    user = models.User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        date_of_birth=data.date_of_birth
    )
    db.add(user)
    db.commit()
    db.refresh(user)


# Email verification endpoints
@router.post("/send-code")
async def send_verification_code(req: schemas.SendCodeRequest, db: db_dependency):
    try:
        Code = oauth2.generate_verification_code()

        # Create a new record
        # not verified by default in the database
        record = models.EmailVerification(
            first_name=req.firstname,
            last_name=req.lastname,
            email=req.email,
            code=Code,
            expires_at = datetime.utcnow() + timedelta(minutes=120)
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        # Send verification code
        await oauth2.send_verification_code(req.email, Code)

        return {"msg": "Verification code sent to email"}
    except Exception as e:
        print("ERROR in /send-code:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-code")
async def verify_verif_code(req: schemas.VerifyCodeRequest, db: db_dependency):
    # Find user by email
    verif_user = db.query(models.EmailVerification).filter(models.EmailVerification.email == req.email).first()

    if not verif_user:
        raise HTTPException(status_code=400, detail="user not found")

    # This is the correct logic for a simple code
    if verif_user.code != req.code:
        raise HTTPException(status_code=400, detail="Invalid code")

    # check if code is expired
    if verif_user.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code expired")

    # Mark user as verified
    verif_user.is_verified = True
    db.commit()
    db.refresh(verif_user)

    # Send confirmation email
    await oauth2.send_confirmation_email(req.email)

    return {"msg": "Email successfully verified"}




# signing up with google
# go to auth/login.py for the callback endpoint
@router.get("/signup/google")
async def signup_google():
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

