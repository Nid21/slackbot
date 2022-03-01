import os
import sqlite3


conn = sqlite3.connect(os.path.join("Slack","users.db"))
c = conn.cursor()

c.execute("SELECT * FROM user")
z = c.fetchall()
print(z)
def create_table():
    global c , conn
    c.execute("CREATE TABLE user(user_id text PRIMARY KEY,username text NOT NULL)")
    conn.commit()

