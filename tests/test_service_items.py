from sqlmodel import SQLModel, Session, create_engine
import pytest

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService

# ------------------------------
# Fixture pour la base en mémoire
# ------------------------------
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# ------------------------------
# Tests pour ItemService
# ------------------------------
def test_create_item(session):
    item_data = ItemCreate(nom="Test Item", prix=9.99)
    item = ItemService.create(session, item_data)
    assert item.id is not None
    assert item.nom == "Test Item"
    assert item.prix == 9.99

def test_get_all_items(session):
    item_data1 = ItemCreate(nom="Item 1", prix=5.0)
    item_data2 = ItemCreate(nom="Item 2", prix=10.0)
    ItemService.create(session, item_data1)
    ItemService.create(session, item_data2)

    items = ItemService.get_all(session, skip=0, limit=10)
    assert len(items) == 2
    assert items[0].nom == "Item 1"
    assert items[1].nom == "Item 2"

def test_get_by_id(session):
    item_data = ItemCreate(nom="Item A", prix=7.5)
    item = ItemService.create(session, item_data)
    fetched_item = ItemService.get_by_id(session, item.id)
    assert fetched_item is not None
    assert fetched_item.nom == "Item A"

def test_update_item(session):
    item_data = ItemCreate(nom="Old Name", prix=5.0)
    item = ItemService.create(session, item_data)
    update_data = ItemUpdate(nom="New Name")
    updated_item = ItemService.update(session, item.id, update_data)
    assert updated_item.nom == "New Name"
    assert updated_item.prix == 5.0  # inchangé

def test_delete_item(session):
    item_data = ItemCreate(nom="Delete Me", prix=1.0)
    item = ItemService.create(session, item_data)
    result = ItemService.delete(session, item.id)
    assert result is True
    # Vérifier que l'item n'existe plus
    assert ItemService.get_by_id(session, item.id) is None

def test_delete_nonexistent_item(session):
    result = ItemService.delete(session, 999)
    assert result is False
