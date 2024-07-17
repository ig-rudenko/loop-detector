from aiohttp.client_exceptions import ClientResponseError
from app.schemas.auth import TokenSchema, LoginSchema, RefreshSchema, VerifySchema, UserSchema
from app.services.auth import get_current_user
from app.services.ecstasy import ecstasy_api
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenSchema)
async def get_token_api_view(user_data: LoginSchema):
    try:
        return await ecstasy_api.get_jwt(user_data)
    except ClientResponseError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.message)


@router.post("/token/verify")
async def verify_token_api_view(data: VerifySchema):
    try:
        verify = await ecstasy_api.verify_jwt(data.token)
    except ClientResponseError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.message)

    if not verify:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/token/refresh", response_model=TokenSchema)
async def refresh_token_api_view(user_data: RefreshSchema):
    try:
        return await ecstasy_api.refresh_jwt(user_data.refresh)
    except ClientResponseError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.message)


@router.get("/myself", response_model=UserSchema)
async def get_user_api_view(user: UserSchema = Depends(get_current_user)):
    return user
