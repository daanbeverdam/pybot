from pybot.helpers.core import CoreHelper


class BirthdayHelper(CoreHelper):
    """Handles database operations for BirthdayCommand."""

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( birthday );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for this command."""
        self.cursor.execute("""
            CREATE TABLE birthday (
                chat_id INTEGER,
                user_id INTEGER,
                date DATE,
                notified_on DATE,
                FOREIGN KEY(chat_id) REFERENCES chats(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def save_birthday(self, chat, user, birthday):
        """Saves birthday, accepts chat and user objects."""
        self.cursor.execute("""
            INSERT INTO birthday
            VALUES (?,?,?,'1-1-1111')
        """, (chat.id, user.id, birthday, ))
        self.save()

    def get_birthday(self, chat, user):
        """Retrieves birthday date, accepts user and chat objects."""
        self.cursor.execute("""
            SELECT date from birthday
            WHERE chat_id=?
            AND user_id=?
        """, (chat.id, user.id))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_birthdays(self, date):
        """Returns all birthday entries for a specific date."""
        self.cursor.execute("""
            SELECT * from birthday
            WHERE date=?
        """, (date,))
        return self.cursor.fetchall()

    def set_notified_at(self, chat_id, user_id, date):
        self.cursor.execute("""
            UPDATE birthday SET notified_on=?
            WHERE chat_id=?
            AND user_id=?
        """, (date, chat_id, user_id))
        self.save()
