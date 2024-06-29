from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from madr.infra import config

engine = create_engine(config.DATABASE_URL)


def get_session() -> Generator[Session, None, None]:  # pragma: no coverage
    with Session(engine) as session:
        yield session
