import sqlite3


class Database:

    def create_database(db: str = "localpasswords.db") -> None:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS passwords(
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
            )
        con.close()

    def read_database(db: str = "localpasswords.db") -> list:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM passwords")
            data = cur.fetchall()
        con.close()
        return data

    def read_database_field(field: str, db: str = "localpasswords.db") -> str:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(f"SELECT {field} FROM passwords")
            data = cur.fetchone()
        con.close()
        return str(data)

    def insert_database(fields: dict, db: str = "localpasswords.db") -> None:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                """INSERT INTO passwords 
                (id, service_name, service_url, username, password, salt)
                VALUES (:id, :service_name, :service_url, :username, :password, :salt)
                """,
                fields,
            )
        con.close()
