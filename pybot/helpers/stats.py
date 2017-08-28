from pybot.helpers.core import CoreHelper


class StatsHelper(CoreHelper):

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( stats );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for this command."""
        self.cursor.execute("""
            CREATE TABLE stats (
            chat_id INTEGER,
            user_id INTEGER,
            words TEXT,
            stickers INTEGER,
            photos TEXT,
            FOREIGN KEY(chat_id) REFERENCES chats(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def collect(self, chat, user, words, sticker, photo):
        self.cursor.execute("""
            SELECT * FROM stats
            WHERE chat_id=?
            AND user_id=?
        """, (chat.id, user.id))
        if not self.cursor.fetchone():
            self.create_entry(chat, user)
        self.cursor.execute("""
            UPDATE stats SET words=words+?, stickers=stickers+?, photos=photos+?
            WHERE chat_id=?
            AND user_id=?
        """, (words, sticker, photo, chat.id, user.id,))
        self.save()

    def create_entry(self, chat, user):
        self.cursor.execute("""
            INSERT INTO stats (chat_id, user_id, words, stickers, photos)
            VALUES (?,?,?,?,?)
        """, (chat.id, user.id, 0, 0, 0,))
        self.save()
