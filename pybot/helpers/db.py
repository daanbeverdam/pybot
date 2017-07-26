import sqlite3
from pybot.env import ROOT_DIR


class DataBase():
    """Handles the most basic database operations."""

    def __init__(self, database=None):
        if not database:
            database = self.get_default_path()

        self.connection = self.connect(database)
        self.cursor = self.get_cursor()
        # TODO: check if tables exist, if not self.create_tables()

    def get_default_path(self):
        return ROOT_DIR + '/etc/database.db'

    def connect(self, database):
        """Opens database connection and returns it."""
        return sqlite3.connect(database)

    def get_cursor(self):
        """Creates new cursor object and returns it."""
        return self.connection.cursor()

    def save(self):
        """Saves the database entries."""
        self.connection.commit()

    def close(self):
        """Saves and closes the database connection."""
        self.connection.commit()
        self.connection.close()
