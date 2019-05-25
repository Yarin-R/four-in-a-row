"""
Helper script to create an empty database
For new servers
"""

import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("""CREATE TABLE users
        (username text, password text, score int)
        """)
conn.commit()
conn.close()
print 'Database users.db created!'
