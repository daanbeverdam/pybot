from pybot.helpers.core import CoreHelper


class KudosHelper(CoreHelper):

    def check_db(self):
        """Will create core tables if they don't exist."""
        self.cursor.execute("""PRAGMA table_info( kudos );""")
        if not self.cursor.fetchone():
            self.create_tables()

    def create_tables(self):
        """Creates tables necessary for kudos command."""
        self.cursor.execute("""CREATE TABLE kudos (
            user_id INTEGER,
            total INTEGER,
            minus INTEGER,
            plus INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
            );""")
        self.save()

    def get_kudos_overview(self, chat):
        """Returns kudo dictionary."""
        kudo_dictionary = {}
        members = self.get_members(chat.id)
        for member in members:
            kudo_dictionary[member.name] = self.get_kudo_count(member)
        return kudo_dictionary

    def get_kudo_count(self, user):
        """Returns kudo count for a user."""
        self.cursor.execute("""
            SELECT total FROM kudos
            WHERE user_id=?
            """, (user.id, ))
        result = self.cursor.fetchone()
        return result

    def kudo_mutation(self, user, no_of_kudos):
        """Adds or substracts kudos for a specific user."""
        pass