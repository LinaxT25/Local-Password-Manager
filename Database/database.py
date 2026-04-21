import sqlite3


class Database:

    __allowed_fields = {
        "id",
        "service_name",
        "service_url",
        "username",
        "password",
        "salt",
    }

    def create_database(db: str = "localpasswords.db") -> None:
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

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
        con.close()

    def read_database(db: str = "localpasswords.db") -> list:
        query = "SELECT * FROM passwords"

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
        con.close()

        return data

    def read_database_field(field: str, db: str = "localpasswords.db") -> str:
        query = f"SELECT {field} FROM passwords"

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchone()
        con.close()

        return str(data)

    def insert_database(self, fields: dict, db: str = "localpasswords.db") -> None:
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

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query, params)
        con.close()

    def update_database(
        self, id: str, fields: dict, db: str = "localpasswords.db"
    ) -> None:
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

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query, params)
        con.close()

    def delete_database(id: str, db: str = "localpasswords.db") -> None:
        params = {"id": id}
        query = "DELETE FROM passwords WHERE id=:id"

        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query, params)
        con.close()
