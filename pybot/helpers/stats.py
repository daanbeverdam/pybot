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
            messages INTEGER,
            words INTEGER,
            stickers INTEGER,
            photos INTEGER,
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
            UPDATE stats SET messages=messages+1, words=words+?,
            stickers=stickers+?, photos=photos+?
            WHERE chat_id=?
            AND user_id=?
        """, (words, sticker, photo, chat.id, user.id,))
        self.save()

    def create_entry(self, chat, user):
        self.cursor.execute("""
            INSERT INTO stats (chat_id, user_id, messages, words, stickers, photos)
            VALUES (?,?,?,?,?,?)
        """, (chat.id, user.id, 0, 0, 0, 0,))
        self.save()

    def get_overview(self, chat):
        self.cursor.execute("""
            SELECT sum(messages), sum(words), sum(stickers), sum(photos) FROM stats
            WHERE chat_id=?
        """, (chat.id,))
        totals = self.cursor.fetchone()
        self.cursor.execute("""
            SELECT user_id, messages, words, stickers, photos FROM stats
            WHERE chat_id=?
        """, (chat.id,))
        user_totals = self.cursor.fetchall()
        overview = {'total': totals}
        for user_total in user_totals:
            user = self.get_user(user_total[0])
            overview[user.first_name] = user_total[1:]
        return overview
