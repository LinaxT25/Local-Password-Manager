import sqlite3
from contextlib import closing


class Database:
    __allowed_fields = {
        "id",
        "service_name",
        "service_url",
        "username",
        "password",
        "salt",
    }

    def __init__(self, db: str = "localpassword.db") -> None:
        self.db = db
        query = """CREATE TABLE IF NOT EXISTS passwords(
                    id TEXT NOT NULL PRIMARY KEY,
                    service_name TEXT NOT NULL,
                    service_url TEXT,
                    username TEXT,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now', 'localtime')),
                    updated_at TEXT DEFAULT (datetime('now', 'localtime'))
                    ) WITHOUT ROWID;
                """

        with closing(sqlite3.connect(db)) as con:
            cur = con.cursor()
            _ = cur.execute(query)

    def read_database(self) -> list:
        query = "SELECT * FROM passwords"

        with closing(sqlite3.connect(self.db)) as con:
            cur = con.cursor()
            _ = cur.execute(query)
            data = cur.fetchall()

        return data

    def read_database_field(self, field: str) -> str:
        query = f"SELECT {field} FROM passwords"

        with closing(sqlite3.connect(self.db)) as con:
            cur = con.cursor()
            _ = cur.execute(query)
            data = cur.fetchone()

        return str(data)

    def insert_database(self, fields: dict) -> None:
        valid_fields = {
            key: value for key, value in fields.items() if key in self.__allowed_fields
        }
        if not valid_fields:
            raise ValueError("No valid fields provided for insert.")

        params = {
            "id": valid_fields.get("id"),
            "service_name": valid_fields["service_name"],
            "service_url": valid_fields.get("service_url"),
            "username": valid_fields.get("username"),
            "password": valid_fields["password"],
            "salt": valid_fields["salt"],
        }

        query = """INSERT INTO passwords
                (id, service_name, service_url, username, password, salt),
                VALUES (:id, :service_name, :service_url, :username, :password, :salt)
                """

        with closing(sqlite3.connect(self.db)) as con:
            cur = con.cursor()
            _ = cur.execute(query, params)

    def update_database(self, id: str, fields: dict) -> None:
        valid_fields = {
            key: value for key, value in fields.items() if key in self.__allowed_fields
        }
        if not valid_fields:
            raise ValueError("No valid fields provided for update.")

        set_clause = ",".join(f"{key}=:{key}" for key in valid_fields)
        params = {"id": id, **valid_fields}

        query = f"""UPDATE passwords
                SET {set_clause}, updated_at=datetime('now', 'localtime')
                WHERE id=:id
                """

        with closing(sqlite3.connect(self.db)) as con:
            cur = con.cursor()
            _ = cur.execute(query, params)

    def delete_database(self, id: str) -> None:
        params = {"id": id}
        query = "DELETE FROM passwords WHERE id=:id"

        with closing(sqlite3.connect(self.db)) as con:
            cur = con.cursor()
            _ = cur.execute(query, params)
