# database upgrade script for v1.0.5 to v1.0.6
from pybot.helpers.core import CoreHelper


def upgrade():
    helper = CoreHelper()
    helper.cursor.execute("""
        ALTER TABLE poll
        ADD COLUMN initiated_at INT
    """)
    helper.save()
    helper.close()

if __name__ == '__main__':
    upgrade()
