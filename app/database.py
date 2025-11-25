"""Configuration de la base de données et gestion des sessions."""

import os
from collections.abc import Generator

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/items_db",
)

POOL_SIZE = 10

engine = create_engine(DATABASE_URL, pool_size=POOL_SIZE)


def get_db() -> Generator[Session]:
    """Créer une session SQLModel pour chaque requête."""
    with Session(engine) as session:
        yield session
