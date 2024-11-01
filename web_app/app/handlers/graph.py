from fastapi import APIRouter, Query, HTTPException, Depends

from app.schemas.auth import UserSchema
from app.schemas.graph import GraphSchema
from app.schemas.graph_info import PaginatedGraphsHistoryInfoSchema
from app.schemas.graph_storage import GraphStorageFileSchema
from app.services.auth import get_current_user
from app.services.graph_info import get_stored_graphs_info, get_stored_graphs_history
from app.services.graph_storage import GraphStorage
from app.services.loop_graph import get_current_loop, GraphException
from app.settings import settings

router = APIRouter(prefix="/graph", tags=["graph"])


def get_params(
    page: int = Query(1, ge=1, le=100, description="Страница"),
    size: int = Query(25, ge=1, le=100, description="Количество элементов на странице"),
):
    return {"page": page, "per_page": size}


@router.get("/current", response_model=GraphSchema)
async def get_current_graph(
    depth: int = Query(1, ge=0, le=5, description="Глубина графа"),
    _: UserSchema = Depends(get_current_user),
):
    try:
        return await get_current_loop(depth)
    except GraphException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.get("/stored", response_model=PaginatedGraphsHistoryInfoSchema)
async def get_stored_graphs(params: dict = Depends(get_params), _: UserSchema = Depends(get_current_user)):
    try:
        return await get_stored_graphs_info(part=params["page"], limit=params["per_page"])
    except GraphStorage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.get("/stored/{name}", response_model=GraphSchema)
async def get_stored_graph_data(name: str, _: UserSchema = Depends(get_current_user)):
    storage = GraphStorage(settings.graph_storage)
    try:
        return await storage.get_storage_file(name)
    except storage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.delete("/stored/{name}", status_code=204)
async def delete_stored_graph_data(name: str, _: UserSchema = Depends(get_current_user)):
    storage = GraphStorage(settings.graph_storage)
    try:
        storage.delete_storage_graph(name)
    except storage.GraphStorageException as exc:
        raise HTTPException(status_code=500, detail=exc.message)


@router.get("/history", response_model=list[GraphStorageFileSchema])
async def get_stored_graph_history(_: UserSchema = Depends(get_current_user)):
    return await get_stored_graphs_history()
