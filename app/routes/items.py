from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_db
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemResponse])
def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[ItemResponse]:
    items = ItemService.get_all(db, skip, limit)
    return [ItemResponse.model_validate(item) for item in items]


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> ItemResponse:
    item = ItemService.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: ItemCreate = Body(...),
    db: Session = Depends(get_db),
) -> ItemResponse:
    return ItemResponse.model_validate(ItemService.create(db, item_data))


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
) -> ItemResponse:
    item = ItemService.update(db, item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
) -> None:
    deleted = ItemService.delete(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
