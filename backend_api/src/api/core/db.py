"""
Database scaffolding for future extension.

This module defines a minimal structure to integrate a database in the future.
Default target is SQLite via SQLAlchemy; however, to keep this step lightweight and
avoid unnecessary dependencies or migrations, we only scaffold the interfaces.

Future steps:
- Add SQLAlchemy models in src/api/models/*.py
- Initialize engine and sessionmaker here
- Add dependency injection for DB sessions in routes
"""
from typing import Optional


class DBSessionManager:
    """
    Placeholder DB session manager.

    Intended lifecycle:
      - On startup, initialize engine and session factory based on DATABASE_URL.
      - Provide get_session dependency for request-scoped DB sessions.
      - Handle graceful teardown.

    For now, this is a stub to signal ready architecture.
    """
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None

    def init(self) -> None:
        """Initialize database engine and session factory (future implementation)."""
        # Example (future):
        # from sqlalchemy import create_engine
        # from sqlalchemy.orm import sessionmaker
        # self.engine = create_engine(self.database_url, connect_args={"check_same_thread": False} if self.database_url.startswith("sqlite") else {})
        # self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return None

    def get_session(self) -> Optional[object]:
        """Provide a database session (future)."""
        # Example (future):
        # db = self.SessionLocal()
        # try:
        #     yield db
        # finally:
        #     db.close()
        return None
