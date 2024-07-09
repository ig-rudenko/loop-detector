from app.schemas.auth import UserSchema
from app.schemas.graph_info import GraphInfoSchema
from app.services.auth import get_current_user
from app.services.graph_info import get_graph_info
from app.services.graph_storage import GraphStorage
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/graph-info", tags=["Graph Info"])


@router.get("/{name}", response_model=GraphInfoSchema)
async def get_stored_graph_data(name: str, _: UserSchema = Depends(get_current_user)):
    try:
        return get_graph_info(name)
    except GraphStorage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=str(exc))
