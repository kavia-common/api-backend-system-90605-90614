from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""
    status: str = Field(..., description="Overall service status indicator.")
    service: str = Field(..., description="Name of the service.")
    version: str = Field(..., description="API version string.")
    theme_primary: str = Field(..., description="Primary theme color hex.")
    theme_secondary: str = Field(..., description="Secondary theme color hex.")


# PUBLIC_INTERFACE
@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Simple health endpoint to verify the API is responsive.",
    responses={
        200: {"description": "Service is healthy and responsive."}
    },
)
def health_check() -> HealthResponse:
    """
    Root health check endpoint.

    Returns:
        HealthResponse: Status payload with theme accents to reflect Ocean Professional branding.
    """
    return HealthResponse(
        status="ok",
        service="Ocean Professional API",
        version="0.1.0",
        theme_primary="#2563EB",
        theme_secondary="#F59E0B",
    )
