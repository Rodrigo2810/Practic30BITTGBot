import sqlite3
from datetime import datetime
from typing import List, Dict

class Database:
    def __init__(self, db_name: str = 'feedback_bot.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_feedback(self, data: Dict):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO feedbacks (rating, name, email, phone, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['rating'], data['name'], data['email'], data['phone'], data['message']))
        self.conn.commit()

    def get_feedbacks(self, limit: int = 10) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT rating, name, email, phone, message, created_at
            FROM feedbacks
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()