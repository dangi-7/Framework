from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./eduapp.db"

def get_engine(echo: bool = False):
    return create_engine(DATABASE_URL, echo=echo, connect_args={"check_same_thread": False})


def init_db(engine=None):
    engine = engine or get_engine()
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    engine = get_engine()
    with Session(engine) as session:
        yield session


@contextmanager
def session_scope():
    engine = get_engine()
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
