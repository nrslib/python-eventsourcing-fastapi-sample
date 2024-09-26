from app.config import setup

setup()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.main import api_router
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
