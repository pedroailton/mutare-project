import sqlite3

class Database:
    def __init__(self, db_path='data/Mutare.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._criar_tabelas()

    def _criar_tabelas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at DATE NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            frequency TEXT,
            motivation TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habit_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE)''')

        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
