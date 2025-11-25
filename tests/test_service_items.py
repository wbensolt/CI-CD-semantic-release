from collections.abc import Generator

import pytest
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.models.item import Item  # Assure-toi d'importer le modèle Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService


@pytest.fixture
def engine() -> Generator[Engine]:
    engine_instance = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine_instance)
    yield engine_instance
    SQLModel.metadata.drop_all(engine_instance)


@pytest.fixture
def session(engine: Engine) -> Generator[Session]:
    with Session(engine) as session_instance:
        yield session_instance


@pytest.fixture
def sample_item_data() -> ItemCreate:
    return ItemCreate(nom="Test Item", prix=10.0)


def test_create_item(session: Session, sample_item_data: ItemCreate) -> None:
    item = ItemService.create(session, sample_item_data)
    assert item.nom == sample_item_data.nom
    assert item.prix == sample_item_data.prix


def test_get_all_items(session: Session, sample_item_data: ItemCreate) -> None:
    ItemService.create(session, sample_item_data)
    items: list[Item] = ItemService.get_all(session, skip=0, limit=10)
    assert len(items) == 1
    assert items[0].nom == sample_item_data.nom


def test_get_by_id(session: Session, sample_item_data: ItemCreate) -> None:
    item = ItemService.create(session, sample_item_data)
    assert item.id is not None
    fetched_item: Item | None = ItemService.get_by_id(session, item.id)
    assert fetched_item is not None
    assert fetched_item.nom == sample_item_data.nom


def test_update_item(session: Session, sample_item_data: ItemCreate) -> None:
    item = ItemService.create(session, sample_item_data)
    assert item.id is not None
    update_data = ItemUpdate(nom="Updated Name", prix=20.0)
    updated_item: Item | None = ItemService.update(session, item.id, update_data)
    assert updated_item is not None
    assert updated_item.nom == "Updated Name"
    assert updated_item.prix == 20.0


def test_delete_item(session: Session, sample_item_data: ItemCreate) -> None:
    item = ItemService.create(session, sample_item_data)
    assert item.id is not None
    result: bool = ItemService.delete(session, item.id)
    assert result is True
    fetched_item: Item | None = ItemService.get_by_id(session, item.id)
    assert fetched_item is None


def test_delete_nonexistent_item(session: Session) -> None:
    result: bool = ItemService.delete(session, 999)
    assert result is False
