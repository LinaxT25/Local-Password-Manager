import sqlite3


class Database:

    def create_database(db="localpasswords.db"):
        con = sqlite3.connect(db)
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
        con.commit()
        con.close()
