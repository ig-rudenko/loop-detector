from fastapi import APIRouter, Depends, Response, HTTPException

from app.schemas.auth import UserSchema
from app.schemas.log_messages import LogMessageSchema
from app.services.auth import get_current_user
from app.services.graph_storage import GraphStorage
from app.services.log_messages import (
    get_current_log_messages,
    delete_current_log_messages,
    get_stored_log_messages,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=list[LogMessageSchema])
async def get_messages(_: UserSchema = Depends(get_current_user)):
    return await get_current_log_messages()


@router.delete("/", status_code=204)
async def delete_messages(user: UserSchema = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete messages")
    await delete_current_log_messages()
    return Response(status_code=204)


@router.get("/stored/{name}", response_model=list[LogMessageSchema])
async def get_stored_messages(name: str, _: UserSchema = Depends(get_current_user)):
    try:
        return await get_stored_log_messages(name)
    except GraphStorage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=str(exc))
