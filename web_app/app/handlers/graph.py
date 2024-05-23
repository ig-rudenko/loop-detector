from app.schemas.auth import UserSchema
from app.schemas.graph import GraphSchema
from app.schemas.graph_storage import GraphStorageFileSchema
from app.services.auth import get_current_user
from app.services.graph_storage import GraphStorage
from app.services.loop_graph import get_current_loop, GraphException
from app.settings import settings
from fastapi import APIRouter, Query, HTTPException, Depends

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/current", response_model=GraphSchema)
async def get_current_graph(
    depth: int = Query(1, ge=0, le=5, description="Глубина графа"),
    _: UserSchema = Depends(get_current_user),
):
    try:
        return await get_current_loop(depth)
    except GraphException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.get("/stored", response_model=list[GraphStorageFileSchema])
async def get_stored_graphs(_: UserSchema = Depends(get_current_user)):
    storage = GraphStorage(settings.graph_storage)
    try:
        return storage.list_storage_files()
    except storage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.get("/stored/{filename}", response_model=GraphSchema)
async def get_stored_graph_data(filename: str, _: UserSchema = Depends(get_current_user)):
    storage = GraphStorage(settings.graph_storage)
    try:
        return storage.get_storage_file(filename)
    except storage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=exc.message)
