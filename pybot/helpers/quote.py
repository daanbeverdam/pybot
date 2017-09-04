from pybot.helpers.core import CoreHelper
import random


class QuoteHelper(CoreHelper):

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( quote );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for this command."""
        self.cursor.execute("""
            CREATE TABLE quote (
            chat_id INTEGER,
            user_id INTEGER,
            name TEXT,
            text TEXT,
            FOREIGN KEY (chat_id) REFERENCES chats(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def save_quote(self, chat, name, quote):
        self.cursor.execute("""
            INSERT INTO quote (name, text)
            VALUES (?,?,?)
        """, (chat.id, name, quote,))
        self.save()

    def get_random_quote(self, chat):
        self.cursor.execute("""
            SELECT name, text FROM quote
            WHERE chat_id=?
        """, (chat.id,))
        results = self.cursor.fetchall()
        if results:
            return random.choice(results)
        return None

    def get_random_quote_by_name(self, chat, name):
        self.cursor.execute("""
            SELECT name, text FROM quote
            WHERE chat_id=?
            AND name=?
        """, (chat.id, name,))
        results = self.cursor.fetchall()
        if results:
            return random.choice(results)
        return None

    def save_quote(self, chat, name, quote):
        self.cursor.execute("""
            INSERT INTO quote (chat_id, name, text)
            VALUES (?,?,?)
        """, (chat.id, name, quote,))
        self.save()

    def get_all_quotes(self, chat):
        self.cursor.execute("""
            SELECT name, text FROM quote
            WHERE chat_id=?
        """, (chat.id,))
        return self.cursor.fetchall()

    def get_all_quotes_by_name(self, chat, name):
        self.cursor.execute("""
            SELECT name, text FROM quote
            WHERE chat_id=?
            AND name=?
        """, (chat.id, name,))
        return self.cursor.fetchall()
