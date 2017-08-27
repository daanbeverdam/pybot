from pybot.helpers.core import CoreHelper


class PollHelper(CoreHelper):

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( poll );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for this command."""
        self.cursor.execute("""
            CREATE TABLE poll (
            id INTEGER,
            chat_id INTEGER,
            question TEXT,
            initiator_id INTEGER,
            flags TEXT,
            PRIMARY KEY(id),
            FOREIGN KEY(chat_id) REFERENCES chats(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE poll_options (
            id INTEGER,
            poll_id INTEGER,
            option TEXT,
            PRIMARY KEY(id),
            FOREIGN KEY(poll_id) REFERENCES poll(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE poll_option_user (
            option_id INTEGER,
            user_id TEXT,
            FOREIGN KEY(option_id) REFERENCES poll_options(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def store_question(self, question, user, chat):
        """Stores poll question, accepts a string and chat object."""
        self.cursor.execute("""
            INSERT INTO poll (chat_id, initiator_id, question)
            VALUES (?,?,?)
        """, (chat.id, user.id, question,))
        self.save()

    def store_options(self, options, chat):
        """Stores poll options, accepts a list of strings and chat object."""
        poll_id = self.get_poll_id(chat)
        for option in options:
            self.cursor.execute("""
                INSERT INTO poll_options (poll_id, option)
                VALUES (?,?)
            """, (poll_id, option,))
        self.save()

    def get_options(self, chat):
        poll_id = self.get_poll_id(chat)
        self.cursor.execute("""
            SELECT option FROM poll_options
            WHERE poll_id=?
        """, (poll_id,))
        results = self.cursor.fetchall()
        options = [result[0] for result in results]
        return options

    def get_initiator(self, chat):
        self.cursor.execute("""
            SELECT initiator_id FROM poll
            WHERE chat_id=?
        """, (chat.id,))
        initiator_id = self.cursor.fetchone()[0]
        return self.get_user(initiator_id)

    def get_poll_id(self, chat):
        self.cursor.execute("""
            SELECT id FROM poll
            WHERE chat_id=?
        """, (chat.id,))
        return self.cursor.fetchone()[0]

    def get_option_id(self, option, poll_id):
        self.cursor.execute("""
            SELECT id FROM poll_options
            WHERE option=?
            AND poll_id=?
        """, (option, poll_id,))
        return self.cursor.fetchone()[0]

    def register_option(self, option, user, chat):
        poll_id = self.get_poll_id(chat)
        option_id = self.get_option_id(option, poll_id)
        self.cursor.execute("""
            INSERT OR IGNORE INTO poll_option_user (option_id, user_id)
            VALUES (?,?)
        """, (option_id, user.id,))
        self.save()
