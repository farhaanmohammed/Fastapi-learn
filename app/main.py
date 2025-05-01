import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from alembic import command
from app.routers import user,auth,posts
from alembic.config import Config
import logging

# Setup logging early
logging.basicConfig(
    level=logging.DEBUG,  # Use DEBUG for full logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)
logger.debug("Logging is configured")

async def run_migrations():
    config = Config("alembic.ini")
    await asyncio.to_thread(command.upgrade,config,"head")

@asynccontextmanager
async  def lifespan(app_: FastAPI):
    await run_migrations()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    logger.info("Root path accessed")
    print("This is a print statement")
    return {"message": "Hello"}



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(posts.router)
