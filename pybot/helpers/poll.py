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
            FOREIGN KEY(poll_id) REFERENCES poll(id) ON DELETE CASCADE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE poll_option_user (
            option_id INTEGER,
            user_id TEXT,
            FOREIGN KEY(option_id) REFERENCES poll_options(id) ON DELETE CASCADE,
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

    def get_question(self, chat):
        self.cursor.execute("""
            SELECT question FROM poll
            WHERE chat_id=?
        """, (chat.id,))
        return self.cursor.fetchone()[0]

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
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

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

    def get_option_ids(self, poll_id):
        """Returns IDs of the active poll."""
        self.cursor.execute("""
            SELECT id FROM poll_options
            WHERE poll_id=?
        """, (poll_id,))
        results = self.cursor.fetchall()
        return [result[0] for result in results]

    def has_voted(self, user, chat):
        """Returns whether an user has voted in chat."""
        poll_id = self.get_poll_id(chat)
        option_ids = self.get_option_ids(poll_id)
        for option_id in option_ids:
            self.cursor.execute("""
                SELECT * FROM poll_option_user
                WHERE user_id=?
                AND option_id=?
            """, (user.id, option_id,))
            result = self.cursor.fetchone()
            if result:
                return True
        return False

    def get_results(self, chat):
        poll_id = self.get_poll_id(chat)
        if poll_id:
            options = self.get_options(chat)
            poll_dict = {}
            for option in options:
                poll_dict[option] = []
            self.cursor.execute("""
                SELECT poll_options.option, poll_option_user.user_id FROM poll_options
                JOIN poll_option_user ON poll_options.id = poll_option_user.option_id
                WHERE poll_options.poll_id = ?;
            """, (poll_id,))
            results = self.cursor.fetchall()
            for option, user_id in results:
                poll_dict[option].append(self.get_user(user_id).first_name)
            return poll_dict
        return None

    def delete_poll(self, chat):
        """Deletes poll and all references for a given chat."""
        # TODO: figure out why on delete cascade is not working
        poll_id = self.get_poll_id(chat)
        self.cursor.execute("""
            DELETE FROM poll
            WHERE id=?
        """, (poll_id,))
        self.cursor.execute("""
            DELETE FROM poll_options
            WHERE poll_id=?
        """, (poll_id,))
        option_ids = self.get_option_ids(poll_id)
        for option_id in option_ids:
            self.cursor.execute("""
                DELETE FROM poll_option_user
                WHERE option_id=?
            """, (option_id,))
        self.save()