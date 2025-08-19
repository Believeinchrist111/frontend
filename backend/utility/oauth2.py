from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import schemas, database, models
from sqlalchemy.orm import Session
from .config import Settings
from database.database import get_db
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


settings = Settings()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='sign-in')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

conf = ConnectionConfig(
    MAIL_USERNAME="you@example.com",
    MAIL_PASSWORD="yourpassword",
    MAIL_FROM="you@example.com",
    MAIL_PORT=587,
    MAIL_SERVER="random.random.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# def verify_access_token(credentials_exception, token: str = Depends(oauth2_bearer)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id = str(payload.get("user_id"))  # Convert user_id to string
#         if id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id=id)
#     except JWTError:
#         raise credentials_exception

#     return token_data

def verify_access_token(token: str = Depends(oauth2_bearer), credentials_exception=None):
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


def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


# we will be using code verification format
def generate_verification_code(length: int = 6) -> str:
    return ''.join(secrets.choice("0123456789") for _ in range(length))

def create_verification_entry(email: str, db: Session, user_id: int):
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    db_verification = EmailVerification(
        user_id=user_id,
        code=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(db_verification)
    db.commit()
    db.refresh(db_verification)
    return code


async def send_verification_code(email: str, code):
    message = MessageSchema(
        subject="email verification",
        recipients=[email],
        body=f"Please enter the 6-digit code to verify your email : {code}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
