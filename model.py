import sqlite3

class UpdateDB:
    def __init__(self, dbname = None):
        if dbname == None:
            dbname = "update.db"
        self.db = sqlite3.connect(dbname)
        self.db.row_factory = sqlite3.Row
        
        self.initSchema()
        pass

    def close(self):
        self.db.close()

    def initSchema(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS update_paths (
          rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
          priority INTEGER,
          mapping TEXT,
          throttle INTEGER,
          update_type TEXT,
          product TEXT,
          version TEXT,
          channel TEXT,
          buildTarget TEXT,
          buildID TEXT,
          locale TEXT,
          osVersion TEXT,
          distribution TEXT,
          distVersion TEXT,
          headerArchitecture TEXT,
          comment TEXT
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS releases (
          name TEXT,
          product TEXT,
          version TEXT,
          data TEXT
        )
        """)

