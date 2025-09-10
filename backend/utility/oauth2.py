from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from database import schemas, database, models
from sqlalchemy.orm import Session
from .config import Settings
from database.database import get_db
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import secrets


settings = Settings()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='sign-in')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# conf = ConnectionConfig(
#     MAIL_USERNAME="you@example.com",
#     MAIL_PASSWORD="yourpassword",
#     MAIL_FROM="you@example.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="random.random.com",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True
# )




# ///////////////////////////////////////////////////////////////////////

# Email verification util functions
def generate_verification_code(length: int = 6) -> str:
    return ''.join(secrets.choice("0123456789") for _ in range(length))


async def send_verification_code(email: str, code: str):
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <h1 style="color: #2c3e50;">Confirm your email address</h1>

        <p>
        There’s one quick step you need to complete before creating your Believe account.
        Let’s make sure that this is the right email address for you –
        please confirm that this is the right address to use for your new account.
        </p>

        <p>
        Please enter this verification code to get started on Believe:
        </p>

        <p style="font-size: 20px; font-weight: bold; color: #e74c3c;">
        {code}
        </p>

        <p>
        Verification codes expire after two hours.
        </p>

        <p>
        Thanks,<br/>
        <b>Believe</b>
        </p>
    </body>
    </html>
    """
                    
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=html_message,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_confirmation_email(email: str):
    message = MessageSchema(
        subject="Email verification successful",
        recipients=[email],
        body="Your email has been successfully verified.",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    
    
    
# //////////////////////////////////////////////////////////////////////



# Sign in authentication util functions    
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception=None):
    if credentials_exception is None:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = str(payload.get("user_id"))  # Convert user_id to string
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data




# /////////////////////////////////////////////////////////////////////

# def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

#     token = verify_access_token(token, credentials_exception)

#     user = db.query(models.User).filter(models.User.id == token.id).first()

#     return user


def get_current_user(
    db: Session = Depends(get_db),
    token: str | None = Cookie(default=None),  # get from cookie only
):
    print('//////////////////////////////////////////')
    print(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token_data = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    print('//////////////////////////////////////////')
    print(user)
    return user
