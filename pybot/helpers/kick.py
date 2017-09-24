from pybot.helpers.core import CoreHelper


class KickHelper(CoreHelper):

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( kick );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for this command."""
        self.cursor.execute("""
            CREATE TABLE kick (
                chat_id INTEGER,
                user_id INTEGER,
                yes_votes INTEGER,
                no_votes INTEGER,
                votes_needed INTEGER,
                FOREIGN KEY(chat_id) REFERENCES chats(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE chat_kick (
                chat_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(chat_id) REFERENCES chats(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def create_entry(self, chat, user, votes_needed):
        self.cursor.execute("""
            INSERT INTO kick
            VALUES (?,?,?,?,?)
        """, (chat.id, user.id, 0, 0, votes_needed, ))
        self.save()

    def remove_entry(self, chat):
        self.cursor.execute("""
            DELETE FROM kick
            WHERE chat_id = ?
        """, (chat.id, ))
        self.cursor.execute("""
            DELETE from chat_kick
            WHERE chat_id = ?
        """, (chat.id, ))
        self.save()

    def register_vote(self, chat, user, vote):
        """Vote can be either 'yes' or 'no'."""
        if vote.lower() == 'yes':
            yes = 1
            no = 0
        elif vote.lower() == 'no':
            yes = 0
            no = 1
        self.cursor.execute("""
            UPDATE kick
            SET yes_votes = yes_votes + ?, no_votes = no_votes +?
            WHERE chat_id = ?
        """, (yes, no, chat.id, ))
        self.cursor.execute("""
            INSERT INTO chat_kick
            VALUES (?, ?)
        """, (chat.id, user.id))
        self.save()

    def has_voted(self, chat, user):
        self.cursor.execute("""
            SELECT * FROM chat_kick
            WHERE chat_id = ?
            AND user_id = ?
        """, (chat.id, user.id))
        if self.cursor.fetchone():
            return True
        return False

    def get_vote_descision(self, chat):
        result = self.get_vote_results(chat)
        if result[0] == result[2]:
            return "kick"
        elif result[1] == result[2]:
            return "keep"
        else:
            return "undecided"

    def get_vote_results(self, chat):
        self.cursor.execute("""
            SELECT yes_votes, no_votes, votes_needed FROM kick
            WHERE chat_id = ?
        """, (chat.id, ))
        return self.cursor.fetchone()

    def get_to_be_kicked_user(self, chat):
        self.cursor.execute("""
            SELECT user_id FROM kick
            WHERE chat_id = ?
        """, (chat.id, ))
        result = self.cursor.fetchone()
        user = self.get_user(result[0])
        return user
