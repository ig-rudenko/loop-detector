from aiohttp.client_exceptions import ClientResponseError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.schemas.auth import UserSchema
from .ecstasy import ecstasy_api

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    try:
        permissions = await ecstasy_api.get_myself_permissions(token)
        if "auth.access_ecstasy_loop" not in permissions:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        user = await ecstasy_api.get_myself(token)
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")

    except ClientResponseError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.message)

    return user


async def get_current_superuser(user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user
