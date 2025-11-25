from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routes import items_router

DEBUG_MODE = True


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Initialisation et fermeture."""
    if DEBUG_MODE:
        SQLModel.metadata.create_all(engine)
    yield


app: FastAPI = FastAPI(lifespan=lifespan)
app.include_router(items_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "API opérationnelle"}
