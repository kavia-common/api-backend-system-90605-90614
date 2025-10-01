from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

# Simple in-memory store to demonstrate behavior; replace with database in future.
_IN_MEMORY_USERS = {}
_NEXT_ID = 1


class UserBase(BaseModel):
    """Common user fields."""
    email: EmailStr = Field(..., description="User email address (unique).")
    full_name: Optional[str] = Field(None, description="Full name of the user.")


class UserCreate(UserBase):
    """Payload for creating a new user."""
    password: str = Field(..., min_length=6, description="User password (min length 6).")


class UserUpdate(BaseModel):
    """Payload for updating an existing user."""
    full_name: Optional[str] = Field(None, description="Updated full name.")
    password: Optional[str] = Field(None, min_length=6, description="Updated password.")


class User(UserBase):
    """User model returned to clients (without storing raw password)."""
    id: int = Field(..., description="User ID.")


def _get_next_id() -> int:
    """Incremental ID generator for in-memory store."""
    global _NEXT_ID
    nid = _NEXT_ID
    _NEXT_ID += 1
    return nid


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description="Creates a new user. Returns basic user details.",
)
def create_user(payload: UserCreate) -> User:
    """
    Create a new user in the system.

    Args:
        payload (UserCreate): User creation payload.

    Returns:
        User: The created user details (excluding password).
    """
    # Validate uniqueness by email for the in-memory store.
    for u in _IN_MEMORY_USERS.values():
        if u["email"].lower() == payload.email.lower():
            raise HTTPException(status_code=409, detail="Email already registered.")
    user_id = _get_next_id()
    # Store the user. NOTE: For demo only; Do not store raw passwords in production.
    _IN_MEMORY_USERS[user_id] = {
        "id": user_id,
        "email": payload.email,
        "full_name": payload.full_name,
        "password": payload.password,  # Placeholder; replace with hashed password in DB integration.
    }
    return User(id=user_id, email=payload.email, full_name=payload.full_name)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[User],
    summary="List users",
    description="Returns a list of users.",
)
def list_users() -> List[User]:
    """
    List all users.

    Returns:
        List[User]: Collection of users (without passwords).
    """
    return [
        User(id=u["id"], email=u["email"], full_name=u.get("full_name"))
        for u in _IN_MEMORY_USERS.values()
    ]


# PUBLIC_INTERFACE
@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get user by ID",
    description="Returns user details for the specified ID.",
)
def get_user(user_id: int) -> User:
    """
    Get a user by ID.

    Args:
        user_id (int): The user identifier.

    Returns:
        User: The requested user.

    Raises:
        HTTPException 404: If the user does not exist.
    """
    u = _IN_MEMORY_USERS.get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found.")
    return User(id=u["id"], email=u["email"], full_name=u.get("full_name"))


# PUBLIC_INTERFACE
@router.patch(
    "/{user_id}",
    response_model=User,
    summary="Update user",
    description="Updates a user's profile fields.",
)
def update_user(user_id: int, payload: UserUpdate) -> User:
    """
    Update fields of a user.

    Args:
        user_id (int): User identifier.
        payload (UserUpdate): Fields to update.

    Returns:
        User: Updated user.

    Raises:
        HTTPException 404: If the user is not found.
    """
    u = _IN_MEMORY_USERS.get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found.")
    if payload.full_name is not None:
        u["full_name"] = payload.full_name
    if payload.password is not None:
        u["password"] = payload.password  # Placeholder; will be hashed in DB phase.
    return User(id=u["id"], email=u["email"], full_name=u.get("full_name"))


# PUBLIC_INTERFACE
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Deletes the specified user.",
)
def delete_user(user_id: int) -> None:
    """
    Delete a user.

    Args:
        user_id (int): The user identifier.

    Returns:
        None

    Raises:
        HTTPException 404: If the user does not exist.
    """
    if user_id not in _IN_MEMORY_USERS:
        raise HTTPException(status_code=404, detail="User not found.")
    del _IN_MEMORY_USERS[user_id]
    return None
