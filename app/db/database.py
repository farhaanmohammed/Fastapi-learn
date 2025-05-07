from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated


DATABASE_URL = "postgresql://postgres:hello123@localhost/FAST_API"

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
