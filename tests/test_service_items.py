import pytest
from sqlmodel import SQLModel, Session, create_engine

from app.schemas.item import ItemCreate, ItemUpdate
from app.services.item_service import ItemService

# ------------------------------
# Fixture pour la base de test
# ------------------------------
@pytest.fixture
def engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session

# ------------------------------
# Fixture pour les données d'un item
# ------------------------------
@pytest.fixture
def sample_item_data():
    return ItemCreate(nom="Test Item", description="A test item", prix=10.0)

# ------------------------------
# Tests CRUD
# ------------------------------
def test_create_item(session, sample_item_data):
    item = ItemService.create(session, sample_item_data)
    assert item.nom == sample_item_data.nom
    assert item.description == sample_item_data.description
    assert item.prix == sample_item_data.prix

def test_get_all_items(session, sample_item_data):
    ItemService.create(session, sample_item_data)
    items = ItemService.get_all(session, skip=0, limit=10)
    assert len(items) == 1
    assert items[0].nom == sample_item_data.nom

def test_get_by_id(session, sample_item_data):
    item = ItemService.create(session, sample_item_data)
    fetched_item = ItemService.get_by_id(session, item.id)
    assert fetched_item is not None
    assert fetched_item.nom == sample_item_data.nom

def test_update_item(session, sample_item_data):
    item = ItemService.create(session, sample_item_data)
    update_data = ItemUpdate(description="Updated description")
    updated_item = ItemService.update(session, item.id, update_data)
    assert updated_item.description == "Updated description"

def test_delete_item(session, sample_item_data):
    item = ItemService.create(session, sample_item_data)
    result = ItemService.delete(session, item.id)
    assert result is True
    assert ItemService.get_by_id(session, item.id) is None

def test_delete_nonexistent_item(session):
    result = ItemService.delete(session, 999)
    assert result is False
