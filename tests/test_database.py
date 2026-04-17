import sqlite3
from Database import database


def test_create_database(db):
    database.Database.create_database(db)

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='passwords';"
        )
        result = cur.fetchone()
    con.close()

    assert result is not None


def test_create_database_structure(db):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("PRAGMA table_info(passwords);")
        columns = cur.fetchall()
        columns_name = [tuples[1] for tuples in columns]
    con.close()

    assert columns_name == [
        "id",
        "service_name",
        "service_url",
        "username",
        "password",
        "salt",
        "created_at",
        "updated_at",
    ]
