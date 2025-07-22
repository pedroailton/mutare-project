import sqlite3
import os

class Database:
    def __init__(self, db_path='data/Mutare.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')
        self.criarTabelas()

    def criarTabelas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Email TEXT NOT NULL,
            nome TEXT NOT NULL,
            criado_em DATE NOT NULL,
            data_inicial DATE NOT NULL,
            data_final DATE NOT NULL,
            frequencia TEXT,
            motivacao TEXT,
            FOREIGN KEY (Email) REFERENCES usuarios(Email) ON DELETE CASCADE)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS habito_progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_habito INTEGER NOT NULL,
            data DATE NOT NULL,
            FOREIGN KEY (id_habito) REFERENCES habitos(id) ON DELETE CASCADE)''')

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
