import sqlite3
from pybot.env import ROOT_DIR
from pybot.core.user import User

class CoreHelper():
    """Handles core operations that are needed for basic bot function."""

    def __init__(self, database=None):
        if not database:
            database = self.get_default_path()
        self.connection = self.connect(database)
        self.cursor = self.get_cursor()
        self.check_db()

    def get_default_path(self):
        return ROOT_DIR + '/etc/database.db'

    def connect(self, database):
        """Opens database connection and returns it."""
        return sqlite3.connect(database)

    def get_cursor(self):
        """Creates new cursor object and returns it."""
        return self.connection.cursor()

    def save(self):
        """Saves the database entries."""
        self.connection.commit()

    def close(self):
        """Saves and closes the database connection."""
        self.connection.commit()
        self.connection.close()

    def check_db(self):
        """Will create and populate core tables if they don't exist."""
        self.cursor.execute("""PRAGMA table_info( core );""")
        if not self.cursor.fetchone():
            print("Creating tables...")
            self.create_tables()
            print ("Populating tables...")
            self.populate_tables()

    def create_tables(self):
        """Creates necessary tables."""
        self.cursor.execute("""CREATE TABLE core ( offset INTEGER );""")
        self.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            );""")
        self.cursor.execute("""
            CREATE TABLE chats (
                id INTEGER PRIMARY KEY,
                title TEXT
            );
            """)
        self.cursor.execute("""
            CREATE TABLE chat_user (
                chat_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(chat_id) REFERENCES chats(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """)
        self.save()

    def populate_tables(self):
        self.cursor.execute("""INSERT INTO core(offset) VALUES(0);""")
        self.save()

    def get_offset(self):
        """Gets offset for long polling."""
        self.cursor.execute("""SELECT offset FROM core""")
        result = self.cursor.fetchone()
        return result[0]

    def set_offset(self, offset):
        """Sets offset for long polling."""
        self.cursor.execute("""UPDATE `core` SET `offset`=?;""", (offset,))
        self.save()

    def get_user(self, id):
        """Gets and returns User object by user ID."""
        self.cursor.execute("""SELECT * FROM users WHERE id=?""", (id,))
        result = self.cursor.fetchone()
        user = User(id=result[0], username=result[1],
                    first_name=result[2], last_name=result[3])
        return user

    def is_known(self, user, chat):
        """Checks if a user-chat combination is in the database."""
        self.cursor.execute("""
            SELECT * FROM chat_user
            WHERE chat_id=?
            AND user_id=?
            """, (chat.id, user.id))
        if self.cursor.fetchone():
            return True
        return False

    def save_user_chat(self, user, chat):
        """Saves user, chat and their relation."""
        self.cursor.execute("""
            INSERT OR IGNORE INTO users (id, username, first_name, last_name)
            VALUES (?,?,?,?)
            """, (user.id, user.username,
                  user.first_name, user.last_name, ))
        self.cursor.execute("""
            INSERT OR IGNORE INTO chats (id, title)
            VALUES (?,?)
            """, (chat.id, chat.title, ))
        self.cursor.execute("""
            INSERT INTO chat_user (chat_id, user_id)
            VALUES (?,?)
            """, (chat.id, user.id, ))
        self.save()

    def get_members(self, id):
        """Get all members of a chat by chat ID."""
        self.cursor.execute("""
            SELECT users.* FROM users
            JOIN chat_user ON users.id = chat_user.user_id
            WHERE chat_user.chat_id=?
            """, (id,))
        results = self.cursor.fetchall()
        users = [User(id=result[0], username=result[1],
                      first_name=result[2], last_name=result[3])
                 for result in results]
        return users
