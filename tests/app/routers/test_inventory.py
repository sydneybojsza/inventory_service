from unittest.mock import patch, ANY
from app.models import User
from app.models.schemas import Inventory

from tests.conftest import (
    _KNOWN_MOCK_USER,
    _KNOWN_MOCK_HASHED_PASSWORD,
    _KNOWN_SWORD_ITEM_NAME,
    _KNOWN_SWORD_ITEM_QUANTITY,
)


@patch("db.crud.add_item")
@patch("routers.inventory.get_current_user")
def test_add_item_to_inventory(mock_get_user, mock_add_item, client, inventory):
    mock_add_item.return_value = inventory
    mock_get_user.return_value = User(
        id=_KNOWN_MOCK_USER, password=_KNOWN_MOCK_HASHED_PASSWORD
    )

    response = client.post(
        "/inventory/add_item/",
        json={
            "item_name": _KNOWN_SWORD_ITEM_NAME,
            "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "item_name": _KNOWN_SWORD_ITEM_NAME,
                "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
            }
        ]
    }

    mock_add_item.assert_called_once()


@patch("db.crud.add_items")
def test_add_items_to_inventory(mock_add_items, client):
    mock_add_items.return_value = Inventory.model_validate(
        {
            "items": [
                {
                    "item_name": _KNOWN_SWORD_ITEM_NAME,
                    "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
                },
                {"item_name": "shield", "quantity": 1},
                {"item_name": "potion", "quantity": 5},
            ]
        }
    )

    response = client.post(
        "/inventory/add_items/",
        json=[
            {"item_name": "shield", "quantity": 1},
            {"item_name": "potion", "quantity": 5},
        ],
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "item_name": _KNOWN_SWORD_ITEM_NAME,
                "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
            },
            {"item_name": "shield", "quantity": 1},
            {"item_name": "potion", "quantity": 5},
        ]
    }

    mock_add_items.assert_called_once()


@patch("db.crud.get_inventory")
def test_get_inventory(mock_get_inventory, client, inventory):
    mock_get_inventory.return_value = inventory
    response = client.get(
        "/inventory/",
    )
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "item_name": _KNOWN_SWORD_ITEM_NAME,
                "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
            },
        ]
    }

    mock_get_inventory.assert_called_with(db=ANY, user_id=_KNOWN_MOCK_USER)


@patch("db.crud.subtract_item")
def test_subtract_item_from_inventory(mock_subtract_item, client, inventory):
    mock_subtract_item.return_value = inventory

    response = client.post(
        "/inventory/subtract_item/",
        json={
            "item_name": _KNOWN_SWORD_ITEM_NAME,
            "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "item_name": _KNOWN_SWORD_ITEM_NAME,
                "quantity": _KNOWN_SWORD_ITEM_QUANTITY,
            },
        ]
    }

    mock_subtract_item.assert_called_once()
