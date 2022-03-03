import sqlite3
#import psycopg2
import os
import json
import random

#conn= psycopg2.connect(
#    host = 'ec2-34-231-183-74.compute-1.amazonaws.com',
#    database = 'dc0igpc5jm4k89',
#    user = 'nfzzdkpylmukuc',
#    password = '7ba6c5d8cb4fde597dd536de44d73f1d6dcfd285ad011e17c5980e0a377a0f67',
#    port = '5432'
#)
#c = conn.cursor()

def log_sql(user_id = None ,name = None ):
    conn = sqlite3.connect(os.path.join("databases","users.db"))
    c = conn.cursor()    
    if user_id == None or name == None:
        return False
	#check if have users
    c.execute("SELECT * FROM botusers where user_id=(?);",(user_id, ))
    #c.execute("SELECT * FROM botuser where user_id=(%s);",(user_id, ))  
    results = c.fetchall()
    if len(results) == 0:   
        c.execute("INSERT INTO botusers (user_id,user_name)VALUES(?,?)", (user_id,name))
        #c.execute("INSERT INTO botuser (user_id,user_name)VALUES(%s,%s )", (user_id,name))
        conn.commit()   
        return True
    else:   
        return False 

def log_sql_qns(dict):
    conn = sqlite3.connect(os.path.join("databases","users.db"))
    c = conn.cursor()
    if len(dict) != 6:
        print(len(dict))
        return False
    else:
        dict1 = json.dumps(dict)
        c.execute("INSERT INTO questions (task_id , question)VALUES (?,?)", (int(dict["qns_task"]),dict1))
        conn.commit()
        #c.execute("INSERT INTO questions (qns,ans_c,ans_w1,ans_w2,ans_w3)VALUES(%s,%s,%s,%s,%s )", (dict["qns_content"], dict["qns_correct"], dict["qns_wrong1"], dict["qns_wrong2"], dict["qns_wrong3"]))
        return True

def select_sql_qns(num = 1 , task = 1):
    conn = sqlite3.connect(os.path.join("databases","users.db"))
    c = conn.cursor()
    c.execute("SELECT qn_id,question FROM questions where task_id=(?)",(task,))
    results = c.fetchall()
    print("results", results)
    random.shuffle(results)
    return results[:num]

def create_table():
    conn = sqlite3.connect(os.path.join("databases","users.db"))
    c = conn.cursor()
    c.execute("CREATE TABLE botusers(user_id text primary key , user_name text)")
    c.execute("CREATE TABLE tasks(task_id INTEGER PRIMARY KEY, task_modal text not null, task_lesson text not null)")
    c.execute("CREATE TABLE results(user_id text NOT NULL, task_id int NOT NULL,qn_id int, completed int NOT NULL, date_sent int NO NULL , result int , option text)")
    c.execute("CREATE TABLE questions(qn_id INTEGER PRIMARY KEY,task_id int not null , question text, FOREIGN KEY(task_id) REFERENCES tasks(task_id))")
    conn.commit()
    #c.execute("""CREATE TABLE botuser(
    #    user_id VARCHAR(20) PRIMARY KEY,
    #    user_name VARCHAR(50) NOT NULL,
    #    created_on TIMESTAMP);""")
    #c.execute(""""CREATE TABLE questions(
    #    qn_id serial PRIMARY KEY,
     #   qn_task TEXT NOT NULL
     #   qns TEXT NOT NULL,
      #  ans_c TEXT NOT NULL,
       # ans_w1 TEXT,
       # ans_w2 TEXT,
       # ans_w3 TEXT,
    #);
    #""")
    #c.execute("""CREATE TABLE results(
    #    user_id VARCHAR(20) NOT NULL,
    #    days_not_replied INT,
    #    qn_id INT NOT NULL,
    #    week INT NOT NULL,
    #    option TEXT NOT NULL,
    #    answered_on TIMESTAMP,
    #    FOREIGN KEY (user_id),
    #        REFERENCES botuser(user_id)
    #    FOREIGN KEY (qn_id)
    #        REFERENCES questions(qn_id)
    #);""")



if __name__ == "__main__":
    create_table()