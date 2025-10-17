from fastapi import Depends, HTTPException, status
from app.db import get_db
from jose import jwt, JWTError
from app.core import settings
from app import crud, models
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


async def require_admin(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role != models.Role.admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user


async def require_worker(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role != models.Role.worker:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Worker privileges required")

    return current_user
