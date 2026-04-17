import pytest
import sqlite3

from Database import database


@pytest.fixture
def db(db="localpasswords.db"):
    return db
