from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

# In-memory entities store, keyed by int id.
_ENTITIES: Dict[int, Dict[str, Any]] = {}
_ENTITIES_NEXT_ID = 1


class EntityBase(BaseModel):
    """Base fields for a generic entity."""
    name: str = Field(..., min_length=1, description="Entity name.")
    description: Optional[str] = Field(None, description="Optional entity description.")


class EntityCreate(EntityBase):
    """Payload to create an entity."""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Arbitrary metadata.")


class EntityUpdate(BaseModel):
    """Payload to update an entity."""
    name: Optional[str] = Field(None, description="Updated entity name.")
    description: Optional[str] = Field(None, description="Updated description.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata map.")


class Entity(EntityBase):
    """Entity returned to clients."""
    id: int = Field(..., description="Entity ID.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata.")


def _entity_next_id() -> int:
    """Generate the next entity ID."""
    global _ENTITIES_NEXT_ID
    v = _ENTITIES_NEXT_ID
    _ENTITIES_NEXT_ID += 1
    return v


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Entity,
    status_code=status.HTTP_201_CREATED,
    summary="Create entity",
    description="Creates a new generic entity.",
)
def create_entity(payload: EntityCreate) -> Entity:
    """
    Create a new generic entity.

    Args:
        payload (EntityCreate): Entity creation payload.

    Returns:
        Entity: The created entity.
    """
    eid = _entity_next_id()
    _ENTITIES[eid] = {
        "id": eid,
        "name": payload.name,
        "description": payload.description,
        "metadata": payload.metadata or {},
    }
    return Entity(**_ENTITIES[eid])


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[Entity],
    summary="List entities",
    description="Returns a list of all entities.",
)
def list_entities() -> List[Entity]:
    """
    List all entities.

    Returns:
        List[Entity]: Collection of entities.
    """
    return [Entity(**e) for e in _ENTITIES.values()]


# PUBLIC_INTERFACE
@router.get(
    "/{entity_id}",
    response_model=Entity,
    summary="Get entity",
    description="Get a single entity by ID.",
)
def get_entity(entity_id: int) -> Entity:
    """
    Retrieve an entity by ID.

    Args:
        entity_id (int): Entity identifier.

    Returns:
        Entity: The requested entity.

    Raises:
        HTTPException 404: If not found.
    """
    e = _ENTITIES.get(entity_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entity not found.")
    return Entity(**e)


# PUBLIC_INTERFACE
@router.patch(
    "/{entity_id}",
    response_model=Entity,
    summary="Update entity",
    description="Update fields on an entity.",
)
def update_entity(entity_id: int, payload: EntityUpdate) -> Entity:
    """
    Update an entity.

    Args:
        entity_id (int): Entity identifier.
        payload (EntityUpdate): Partial update payload.

    Returns:
        Entity: Updated entity.

    Raises:
        HTTPException 404: If not found.
    """
    e = _ENTITIES.get(entity_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entity not found.")

    if payload.name is not None:
        e["name"] = payload.name
    if payload.description is not None:
        e["description"] = payload.description
    if payload.metadata is not None:
        e["metadata"] = payload.metadata

    return Entity(**e)


# PUBLIC_INTERFACE
@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete entity",
    description="Deletes the specified entity.",
)
def delete_entity(entity_id: int) -> None:
    """
    Delete an entity.

    Args:
        entity_id (int): Entity identifier.

    Returns:
        None

    Raises:
        HTTPException 404: If not found.
    """
    if entity_id not in _ENTITIES:
        raise HTTPException(status_code=404, detail="Entity not found.")
    del _ENTITIES[entity_id]
    return None
