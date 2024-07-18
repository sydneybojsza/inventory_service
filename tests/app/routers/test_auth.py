from unittest.mock import patch, ANY, Mock
from models import User


_KNOWN_MOCK_USER: str = "mockuser"
_KNOWN_MOCK_PASSWORD: str = "mockpassword"
_KNOWN_MOCK_HASHED_PASSWORD: str = f"fakehashed{_KNOWN_MOCK_PASSWORD}"


@patch("routers.auth.authenticate_user")
@patch("routers.auth.get_user")
def test_login(mock_get_user: Mock, mock_authenticate_user: Mock, client):
    mock_get_user.return_value = User(
        id=_KNOWN_MOCK_USER, password=_KNOWN_MOCK_HASHED_PASSWORD
    )
    mock_authenticate_user.return_value = User(
        id=_KNOWN_MOCK_USER, password=_KNOWN_MOCK_HASHED_PASSWORD
    )

    response = client.post(
        "/token",
        data={"username": _KNOWN_MOCK_USER, "password": _KNOWN_MOCK_HASHED_PASSWORD},
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": _KNOWN_MOCK_USER,
        "token_type": "bearer",
    }

    mock_authenticate_user.assert_called_with(
        ANY, _KNOWN_MOCK_USER, _KNOWN_MOCK_HASHED_PASSWORD
    )
