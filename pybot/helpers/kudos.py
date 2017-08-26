from pybot.helpers.core import CoreHelper


class KudosHelper(CoreHelper):

    def check_db(self):
        """Checks if necessary tables exist."""
        self.cursor.execute("""PRAGMA table_info( kudos );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for kudos command."""
        self.cursor.execute("""
            CREATE TABLE kudos (
            user_id INTEGER,
            total INTEGER,
            minus INTEGER,
            plus INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.save()

    def create_user_row(self, user):
        """Creates kudos entry for specific user."""
        self.cursor.execute("""
            INSERT INTO kudos
            (user_id, total, minus, plus)
            VALUES (?, ?, ?, ?);
            """, (user.id, 0, 0, 0, ))
        self.save()

    def get_kudos_dict(self, chat):
        """Returns kudo dictionary."""
        kudo_dictionary = {}
        members = self.get_members(chat)
        for member in members:
            kudo_count = self.get_kudo_count(member)
            if kudo_count:
                kudo_dictionary[member.first_name] = self.get_kudo_count(member)
        return kudo_dictionary

    def get_kudo_count(self, user):
        """Returns kudo count for a user."""
        self.cursor.execute("""
            SELECT total FROM kudos
            WHERE user_id=?;
            """, (user.id, ))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return result

    def mutate_kudos(self, user, no_of_kudos):
        """Adds or substracts kudos for a specific user."""
        current_kudos = self.get_kudo_count(user)
        if current_kudos is not None:
            new_kudos = current_kudos + no_of_kudos
            self.cursor.execute("""UPDATE kudos
                SET total=?
                WHERE user_id=?;
                """, (new_kudos, user.id, ))
            self.save()
            # TODO: set minus / plus
        else:
            self.create_user_row(user)
            self.mutate_kudos(user, no_of_kudos)
