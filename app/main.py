import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager
from alembic import command
from app.routers import user,auth,posts
from alembic.config import Config
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from .exception_handlers  import request_validation_exception_handler, http_exception_handler, unhandled_exception_handler
from .middleware import log_request_middleware




async def run_migrations():
    config = Config("alembic.ini")
    await asyncio.to_thread(command.upgrade,config,"head")

@asynccontextmanager
async  def lifespan(app_: FastAPI):
    await run_migrations()
    yield


app = FastAPI(lifespan=lifespan)

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(posts.router)
