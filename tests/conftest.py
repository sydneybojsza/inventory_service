import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models import Base, User
from dependencies import get_current_user, get_db
from models.schemas import Inventory, InventoryItem, ItemCreate

# In-memory SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_KNOWN_MOCK_USER: str = "mockuser"
_KNOWN_MOCK_PASSWORD: str = "mockpassword"
_KNOWN_MOCK_HASHED_PASSWORD: str = f"fakehashed{_KNOWN_MOCK_PASSWORD}"
_KNOWN_SWORD_ITEM_NAME: str = "sword"
_KNOWN_SWORD_ITEM_QUANTITY: int = 1


def setup_database():
    db = TestingSessionLocal()
    # Create all tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    user = User(id=_KNOWN_MOCK_USER, password=_KNOWN_MOCK_HASHED_PASSWORD)
    db.add(user)
    db.commit()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def unauthenticated_client():
    app.dependency_overrides[get_db] = setup_database
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def client():
    def override_get_current_user():
        return _KNOWN_MOCK_USER

    app.dependency_overrides[get_db] = setup_database
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as c:
        yield c


@pytest.fixture
def inventory_item():
    return InventoryItem(
        item_name=_KNOWN_SWORD_ITEM_NAME, quantity=_KNOWN_SWORD_ITEM_QUANTITY
    )


@pytest.fixture
def item_create():
    return ItemCreate(
        item_name=_KNOWN_SWORD_ITEM_NAME, quantity=_KNOWN_SWORD_ITEM_QUANTITY
    )


@pytest.fixture
def inventory(inventory_item):
    return Inventory(items=[inventory_item])


@pytest.fixture
def user(inventory):
    return User(
        id=_KNOWN_MOCK_USER, password=_KNOWN_MOCK_HASHED_PASSWORD, inventory=inventory
    )
