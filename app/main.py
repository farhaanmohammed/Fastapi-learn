import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from alembic import command
from app.routers import user,auth,posts
from alembic.config import Config
from loguru import logger


async def run_migrations():
    config = Config("alembic.ini")
    await asyncio.to_thread(command.upgrade,config,"head")

@asynccontextmanager
async  def lifespan(app_: FastAPI):
    await run_migrations()
    yield


app = FastAPI(lifespan=lifespan)
logger.info("App started")

@app.get("/")
async def read_root():
    logger.info("Hello")
    print("This is a print statement")
    return {"message": "Hello"}



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(posts.router)
