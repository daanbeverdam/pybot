# database upgrade script for v1.0.0 to v1.0.1
from pybot.helpers.core import CoreHelper


def upgrade():
    helper = CoreHelper()
    helper.cursor.execute("""
            SELECT offset FROM core;
        """)
    offset = helper.cursor.fetchone()[0]
    helper.cursor.execute("""
            DROP TABLE core;
        """)
    helper.save()
    helper.cursor.execute("""
            CREATE TABLE core (
                variable TEXT,
                value TEXT
            );
        """)
    helper.save()
    helper.cursor.execute("""
            INSERT INTO core(variable, value)
            VALUES ("offset", ?)
        """, (offset, ))
    helper.save()
    helper.close()

if __name__ == '__main__':
    upgrade()
