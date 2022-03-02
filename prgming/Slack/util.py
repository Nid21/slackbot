import os
import sqlite3
import schedule
import time
import asyncio
def create_table():
    global c , conn
    c.execute("CREATE TABLE user(user_id text PRIMARY KEY,username text NOT NULL)")
    conn.commit()
conn = sqlite3.connect("users.db")
c = conn.cursor()

create_table()
c.execute("SELECT * FROM user")
z = c.fetchall()
print(z)


def gay(num):
    print(num)

schedule.every(1).seconds.do(gay, "gay")

async def sch():
    for i in range(20):
        schedule.run_pending()
        await asyncio.sleep(3)

async def randtask():
    for i in range(10):
        print("here",i)
        print(i)
        await asyncio.sleep(5)
        print("next",i)

async def main():
    t2 = asyncio.create_task(randtask())
    t1 = asyncio.create_task(sch())
    
    await t1
    await t2

asyncio.run(main())
    