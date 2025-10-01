from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from .routers import health, users, entities
from .core.settings import get_settings

# Initialize settings (reads from environment via pydantic)
settings = get_settings()

# Configure FastAPI application with metadata aligned to "Ocean Professional" theme.
app = FastAPI(
    title="Ocean Professional API",
    description=(
        "Modern RESTful API with a clean aesthetic and minimalist design.\n\n"
        "Theme: Ocean Professional (blue & amber accents)\n\n"
        "Use endpoints grouped by purpose: Health, Users, Entities.\n"
        "This API is scaffolded for future expansion and database integration."
    ),
    version="0.1.0",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "Health", "description": "Health and readiness checks."},
        {"name": "Users", "description": "User management endpoints."},
        {"name": "Entities", "description": "Generic data entity management endpoints."},
        {"name": "Docs", "description": "Documentation and usage information."},
    ],
)

# CORS configuration with safe defaults and extensibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    """
    Build a custom OpenAPI schema to reflect theme accents and inject branding metadata.
    This function does not change endpoint behavior—only the documentation appearance and metadata.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Inject theme details so consumers and doc renderers can optionally style with these hints.
    openapi_schema["x-theme"] = {
        "name": "Ocean Professional",
        "primary": "#2563EB",
        "secondary": "#F59E0B",
        "error": "#EF4444",
        "background": "#f9fafb",
        "surface": "#ffffff",
        "text": "#111827",
        "gradient": "from-blue-500/10 to-gray-50",
        "style": "modern-minimalist",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Use custom OpenAPI generator
app.openapi = custom_openapi

# Register routers with clear prefixes and tags
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(entities.router, prefix="/entities", tags=["Entities"])


# PUBLIC_INTERFACE
@app.get(
    "/docs/usage",
    summary="API usage instructions",
    description=(
        "Provides a brief overview of how to use the API and notes on the Ocean Professional theme.\n\n"
        "For WebSocket usage (if/when added), connect via documented ws routes; currently there are none. "
        "This endpoint exists to anchor documentation and project-level usage notes."
    ),
    tags=["Docs"],
)
def get_usage_info():
    """
    This endpoint returns basic usage information for the API.
    Returns a structure with theme hints and pointers to the OpenAPI docs.
    """
    return {
        "message": "Welcome to the Ocean Professional API",
        "theme": {
            "name": "Ocean Professional",
            "primary": "#2563EB",
            "secondary": "#F59E0B",
        },
        "docs": {
            "openapi_json": "/openapi.json",
            "swagger_ui": "/docs",
            "redoc": "/redoc",
        },
        "notes": "Use health, users, and entities endpoints as starting points. Database layer is scaffolded for SQLite."
    }
