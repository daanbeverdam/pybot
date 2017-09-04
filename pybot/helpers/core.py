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
        self.cursor.execute("""PRAGMA foreign_keys = ON""")
        self.save()
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
            CREATE TABLE bot (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT
            );
            """)
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
        self.cursor.execute("""
            CREATE TABLE commands (
            chat_id INTEGER,
            name TEXT,
            active INTEGER,
            waiting INTEGER,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
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

    def get_user_by_name(self, name, chat):
        """Finds a user by name in a certain chat.
        May be inaccurate, get_user() by id is preferred."""
        self.cursor.execute("""
            SELECT users.* FROM users
            JOIN chat_user ON users.id = chat_user.user_id
            WHERE chat_user.chat_id=?
            AND users.first_name LIKE ?
            OR users.last_name LIKE ?
            """, (chat.id, name, name, ))
        result = self.cursor.fetchall()
        if len(result) == 1:
            result = result[0]
            return User(id=result[0], username=result[1],
                        first_name=result[2], last_name=result[3])
        bot = self.get_self()
        if bot.first_name.lower() == name.lower():
            return bot
        return None

    def is_known(self, user, chat):
        """Checks if a user-chat combination is in the database."""
        self.cursor.execute("""
            SELECT * FROM chat_user
            WHERE chat_id=?
            AND user_id=?
            """, (chat.id, user.id, ))
        if self.cursor.fetchone():
            return True
        return False

    def save_self(self, bot):
        """Saves bot."""
        if not self.get_self():
            self.cursor.execute("""
                INSERT OR IGNORE INTO bot (id, first_name, username)
                VALUES (?,?,?)
                """, (bot.id, bot.first_name,
                      bot.username ))
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (id, first_name, username)
                VALUES (?,?,?)
                """, (bot.id, bot.first_name,
                      bot.username ))
        else:
            self.cursor.execute("""
            UPDATE bot
            SET first_name=?, username=?
            """, (bot.first_name,
                  bot.username ))
            self.cursor.execute("""
            UPDATE users
            SET first_name=?, last_name=?, username=?
            WHERE id=?
            """, (bot.first_name, bot.last_name,
                  bot.username, bot.id, ))
        self.save()

    def get_self(self):
        """Returns bot info in as User object."""
        self.cursor.execute("""SELECT * FROM bot""")
        result = self.cursor.fetchone()
        if result:
            bot = User(id=result[0], first_name=result[1], username=result[2])
            return bot
        return None

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

    def update_user_chat(self, user, chat):
        """Updates user and chat values."""
        self.cursor.execute("""
            UPDATE users
            SET first_name=?, last_name=?, username=?
            WHERE id=?
            """, (user.first_name, user.last_name,
                  user.username, user.id, ))
        self.cursor.execute("""
            UPDATE chats
            SET id=?, title=?
            WHERE id=?
        """, (chat.id, chat.title, chat.id))
        self.save()

    def get_members(self, chat, include_self=True):
        """Get all members of a chat. Accepts Chat object."""
        self.cursor.execute("""
            SELECT users.* FROM users
            JOIN chat_user ON users.id = chat_user.user_id
            WHERE chat_user.chat_id=?
            """, (chat.id,))
        results = self.cursor.fetchall()
        users = [User(id=result[0], username=result[1],
                      first_name=result[2], last_name=result[3])
                 for result in results]
        if include_self:
            users.append(self.get_self())
        return users

    def command_is_active(self, chat, name):
        self.cursor.execute("""
            SELECT active FROM commands
            WHERE chat_id=?
            AND name=?
            """, (chat.id, name,))
        status = self.cursor.fetchone()
        if status:
            return status[0]
        else:
            self.create_command_row(chat, name)
            return self.command_is_active(chat, name)

    def activate_command(self, chat, name, status):
        self.cursor.execute("""
            UPDATE commands
            SET active=?
            WHERE chat_id=?
            AND name=?;
            """, (status, chat.id, name,))
        self.save()

    def create_command_row(self, chat, name):
        self.cursor.execute("""
            INSERT INTO commands(chat_id, name, active, waiting)
            VALUES (?, ?,?,?)
            """, (chat.id, name, 0, 0,))
        self.save()
