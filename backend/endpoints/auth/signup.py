from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette import status
from database.database import get_db
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





# Endpoint for signing up or creating an account

# Email verification endpoints
@router.post("/send-code")
async def send_token(req: schemas.SendCodeRequest, db: db_dependency):
    try:
        code = oauth2.generate_verification_code()

        # Create a new record
        record = models.EmailVerification(
            firstname=req.firstname,
            lastname=req.lastname,
            email=req.email,
            code=code,
            verified=False,
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=120)
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # Send verification email
        await oauth2.send_verification_code(req.email, code)

        return {"msg": "Verification token sent to email"}
    except Exception as e:
        print("ERROR in /send-code:", e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/verify-code")
async def verify_user_token(req: schemas.VerifyCodeRequest, db: db_dependency):
    # Find user by email
    user = db.query(models.EmailVerification).filter(models.EmailVerification.email == req.email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.code != req.code:
        raise HTTPException(status_code=400, detail="Invalid code")
    
    # expires_at = user.expires_at
    # if expires_at.tzinfo is None:  # naive -> make it aware
    #     expires_at = expires_at.replace(tzinfo=timezone.utc)
    # if user.expires_at < datetime.now(timezone.utc):
    #     raise HTTPException(status_code=400, detail="Verification code expired")

    # Mark user as verified
    user.verified = True
    db.commit()
    db.refresh(user)
    
    # Send confirmation email
    await oauth2.send_confirmation_email(req.email)

    return {"msg": "Email successfully verified"}



@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user: schemas.UserCreate, db: db_dependency):
    print(user.firstname)
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create JWT
    access_token = oauth2.create_access_token(data={"user_id": new_user.id})

    response = JSONResponse(content={
        "message": "Signup successful",
        "user": {
            "id": new_user.id,
            "firstname": new_user.firstname,
            "lastname": new_user.lastname,
            "email": new_user.email,
        },
        "access_token": access_token,
        "token_type": "bearer",
    })

    # set cookie so middleware sees it
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        secure=False,   # set True in production
        samesite="lax",
        max_age=30 * 60,
    )
    return response
    
# ////////////////////////////////////////////////////////////////////



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

