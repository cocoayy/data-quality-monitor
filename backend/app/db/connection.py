from collections.abc import Generator

from psycopg import connect
from psycopg.rows import dict_row

from app.config import settings


def get_connection():
    return connect(settings.database_url, row_factory=dict_row)


def get_db() -> Generator:
    with get_connection() as conn:
        yield conn
