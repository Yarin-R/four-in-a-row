import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("""CREATE TABLE users
        (username text, password text)
        """)
conn.commit()
conn.close()
print 'Database users.db created!'
