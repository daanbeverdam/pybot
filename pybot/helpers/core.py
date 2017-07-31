from pybot.helpers.db import DataBase
from pybot.core.user import User


class Core(DataBase):
    """Handles core operations that are needed for basic bot function."""

    def check_db(self):
        self.cursor.execute("PRAGMA table_info( core );")
        if not self.cursor.fetchone():
            print("Creating tables...")
            self.create_tables()
            print ("Populating tables...")
            self.populate_tables()

    def create_tables(self):
        """Creates necessary tables."""
        self.cursor.execute("CREATE TABLE `core` ( `offset` INTEGER );")
        self.cursor.execute("""CREATE TABLE `users` ( `id` INTEGER,
                                                      `username` TEXT,
                                                      `first_name` TEXT,
                                                      `last_name` TEXT,
                                                       UNIQUE(id)
                                                    );""")
        self.cursor.execute("CREATE TABLE `chats` ( `id` INTEGER, `title` TEXT );")
        self.cursor.execute("CREATE TABLE `chat_user` ( `chat_id` INTEGER, `user_id` INTEGER );")
        self.save()

    def populate_tables(self):
        self.cursor.execute("INSERT INTO core(offset) VALUES(1);")
        self.save()

    def get_offset(self):
        """Gets offset for long polling."""
        self.cursor.execute("SELECT offset FROM core")
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0

    def set_offset(self, offset):
        """Sets offset for long polling."""
        self.cursor.execute("UPDATE `core` SET `offset`=?;", (offset,))
        self.save()

    def get_user(self, id):
        """Gets and returns User object by user ID."""
        self.cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        result = self.cursor.fetchone()
        user = User(id=result[0], username=result[1],
                    first_name=result[2], last_name=result[3])
        return user

    def save_user(self, user, chat):
        self.cursor.execute("""INSERT OR IGNORE INTO users (id, username, first_name, last_name)
                            VALUES (?,?,?,?)""", (user.id, user.username, user.first_name, user.last_name, ))
        self.save()

    def get_members(self, id):
        """Get all members of a chat by chat ID."""
        self.cursor.execute("""SELECT users.* FROM users
                            JOIN chat_user ON users.id = chat_user.user_id
                            WHERE chat_user.chat_id=?""", (id,))
        results = self.cursor.fetchall()
        users = [User(id=result[0], username=result[1],
                      first_name=result[2], last_name=result[3])
                 for result in results]
        return users
