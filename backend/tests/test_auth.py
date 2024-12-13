import jwt
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, Mock

from app.core.auth.services import authenticate_user, register_user, login_user
from app.core.auth.utils import create_access_token
from app.core.users.models import UserDB
from app.core.users.exceptions import (
    InvalidPasswordException,
    UserDoesNotExistException,
    EmailAlreadyExistsException,
)
from app.core.auth.schemas import RegisterRequest
from app.config import config


@pytest.fixture
def mock_user_db(mocker):
    mocker.patch("app.core.users.models.UserDB.get_or_none", AsyncMock())
    mocker.patch("app.core.users.models.UserDB.create", AsyncMock())


@pytest.fixture
def mock_password_verification(mocker):
    mocker.patch(
        "app.core.users.models.UserDB.verify_password", AsyncMock(return_value=True)
    )


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_user_db, mock_password_verification):
    # Arrange
    mock_user = AsyncMock()
    mock_user.email = "test@example.com"
    UserDB.get_or_none.return_value = mock_user
    mock_user.verify_password = Mock(return_value=True)

    # Act
    user = await authenticate_user("test@example.com", "password123")

    # Assert
    assert user.email == "test@example.com"
    UserDB.get_or_none.assert_called_once_with(email="test@example.com")
    mock_user.verify_password.assert_called_once_with("password123")


@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(mock_user_db):
    # Arrange
    UserDB.get_or_none.return_value = None

    # Act & Assert
    with pytest.raises(UserDoesNotExistException):
        await authenticate_user("nonexistent@example.com", "password123")


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(mocker):
    # Arrange
    mock_user = Mock()
    mock_user.email = "test@example.com"
    mock_user.verify_password = Mock(return_value=False)
    mocker.patch(
        "app.core.users.models.UserDB.get_or_none", AsyncMock(return_value=mock_user)
    )

    # Act & Assert
    with pytest.raises(InvalidPasswordException):
        await authenticate_user("test@example.com", "wrongpassword")


@pytest.mark.asyncio
async def test_register_user_success(mocker):
    # Arrange
    register_request = RegisterRequest(
        name="John Doe", email="newuser@example.com", password="password123"
    )

    mocker.patch(
        "app.core.users.models.UserDB.get_or_none", AsyncMock(return_value=None)
    )

    mock_created_user = AsyncMock()
    mock_created_user.id = 1
    mocker.patch(
        "app.core.users.models.UserDB.create", AsyncMock(return_value=mock_created_user)
    )
    mocker.patch(
        "app.core.users.models.UserDB.get", AsyncMock(return_value=mock_created_user)
    )

    # Act
    user = await register_user(register_request)

    # Assert
    assert user == mock_created_user
    UserDB.get_or_none.assert_called_once_with(email="newuser@example.com")
    UserDB.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_email_exists(mock_user_db):
    # Arrange
    register_request = RegisterRequest(
        name="John Doe", email="existing@example.com", password="password123"
    )
    UserDB.get_or_none.return_value = AsyncMock()

    # Act & Assert
    with pytest.raises(EmailAlreadyExistsException):
        await register_user(register_request)


@pytest.mark.asyncio
async def test_login_user_success(mocker):
    # Arrange
    mock_user = Mock()
    mock_user.email = "test@example.com"
    mock_user.verify_password = Mock(return_value=True)
    mocker.patch(
        "app.core.users.models.UserDB.get_or_none", AsyncMock(return_value=mock_user)
    )
    mocker.patch(
        "app.core.auth.services.create_access_token", return_value="mock_token"
    )

    # Act
    token_response = await login_user("test@example.com", "password123")

    # Assert
    assert token_response.access_token == "mock_token"
    UserDB.get_or_none.assert_called_once_with(email="test@example.com")
    mock_user.verify_password.assert_called_once_with("password123")


@pytest.mark.asyncio
async def test_login_user_user_not_found(mock_user_db):
    # Arrange
    UserDB.get_or_none.return_value = None

    # Act & Assert
    with pytest.raises(UserDoesNotExistException):
        await login_user("nonexistent@example.com", "password123")


@pytest.mark.asyncio
async def test_create_access_token():
    # Arrange
    data = {"sub": "test@example.com"}
    expires = timedelta(minutes=30)

    # Act
    token = create_access_token(data, expires)

    # Assert
    assert isinstance(token, str)
    decoded_token = jwt.decode(
        token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
    )
    assert decoded_token["sub"] == "test@example.com"
    assert decoded_token.get("exp") is not None
    expiry_delta = datetime.fromtimestamp(
        decoded_token["exp"], timezone.utc
    ) - datetime.now(timezone.utc)
    assert pytest.approx(expiry_delta.total_seconds(), 7) == expires.total_seconds()
