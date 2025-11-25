import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv(".env")

# Récupérer la base de données depuis les secrets ou variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set in environment variables")

POOL_SIZE = int(os.getenv("POOL_SIZE", 10))

engine = create_engine(DATABASE_URL, pool_size=POOL_SIZE)


def get_db() -> Generator[Session]:
    """Créer une session SQLModel pour chaque requête."""
    with Session(engine) as session:
        yield session
