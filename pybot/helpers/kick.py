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
        self.save()

    def register_vote(self, chat, vote):
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
        self.save()

    def get_vote_results(self, chat):
        self.cursor.execute("""
            SELECT yes_votes, no_votes, votes_needed FROM kick
            WHERE chat_id = ?
        """, (chat.id, ))
        result = self.cursor.fetchone()
        if result[0] == result[2]:
            return "kick"
        elif result[1] == result[2]:
            return "keep"
        else:
            return "undecided"

    def get_to_be_kicked_user(self, chat):
        self.cursor.execute("""
            SELECT user_id FROM kick
            WHERE chat_id = ?
        """, (chat.id, ))
        result = self.cursor.fetchone()
        user = self.get_user(result[0])
        return user
