from pybot.helpers.db import DataBase


class Core(DataBase):
    """Handles core operations that are needed for basic bot function."""

    def create_tables(self):
        """Creates necessary tables."""
        self.cursor.execute("CREATE TABLE `core` ( `offset` INTEGER );")
        self.cursor.execute("CREATE TABLE `users` ( `id` INTEGER, `username` TEXT, `first_name` TEXT, `last_name` TEXT );")
        self.cursor.execute("CREATE TABLE `chats` ( `id` INTEGER, `title` TEXT );")
        self.cursor.execute("CREATE TABLE `chat_user` ( `chat_id` INTEGER, `user_id` INTEGER );")

    def get_offset(self):
        """Gets offset for long polling."""
        self.cursor.execute("SELECT offset FROM core")
        return self.cursor.fetchone()[0]

    def set_offset(self, offset):
        self.cursor.execute("UPDATE `core` SET `offset`=?;", (offset,))

    def get_user(self, id):
        """Gets and returns user by Telegram ID."""
        self.cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        return self.cursor.fetchone()
