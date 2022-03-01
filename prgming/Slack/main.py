code = "xapp-1-A034FAQDDDM-3168440167236-e2f1e3734c3311e88ba448bd0e4187a34f89a48137174e767b968e45b6c0c557"
token = "xoxb-3165462542083-3165963183010-EArtapJ8aizdSqJJy5Ebkxux"
import sqlite3
import datetime
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
conn = sqlite3.connect(os.path.join("Slack","users.db"))
c = conn.cursor()

_id = {}
app = App(token = token)

@app.event("team_join")
def ask_for_introduction(event, say):
	welcome_channel_id = "C034PA3SNF8"
	user_id = event["user"]
	text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
	say(text=text, channel=welcome_channel_id)
	users = app.client.users_list()
	username = users["members"]["name"] if users["members"]["id"] == user_id else None
	if not log_sql(user_id = user_id, name = username):
		print("log new user error")

@app.command("/joke")
def joke(say, client, ack):
	ack()
	jokes = set(["//be nice to the CPU\nThread_sleep(1);" , "!false\n(It's funny because it's true.)" ,"What did the router say to the doctor?\n'It hurts when IP'","Nidhish"])
	say(jokes.pop())
	time = datetime.datetime.now()+datetime.timedelta(seconds=20)
	time = int(time.timestamp())

	client.chat_scheduleMessage(channel="U035K656K3J",text="Looking towards the future",post_at=time)
	result = client.chat_scheduledMessages_list()
        # Print scheduled messages
	for message in result["scheduled_messages"]:
		print(message)

@app.event("app_mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
def mention_handler(body, say):
        say(blocks=[
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Hi, welcome to the employee training programme.\n Click the button below for today's task!:smile:",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Tasks",
						"emoji": True
					},
					"value": "task",
					"action_id": "taskmaster"
				}
			]
		}
	]
)

@app.action("taskmaster")
def task_handler(ack , respond):
    ack()
    task = "random task"
    respond( blocks = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": f"Your task for today will be: {task}.\n Once done please press the button done :smile:",
				"emoji": True
			}
		},
        {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Done",
						"emoji": True
					},
					"value": "Done",
                    "style": "primary",
					"action_id": "Donetask"
				}
			]
		}
	]
)

@app.action("Donetask")
def finished(ack, respond):
    ack()
    respond(blocks = [
        {
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Thank you for finishing your work!",
				"emoji": True
			}
		},{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Another task"
					},
					"style": "primary",
					"value": "click_me_123",
                    "action_id": "taskmaster"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Deny"
					},
					"style": "danger",
					"value": "click_me_123",
                    "action_id": "Done"
				}
			]
		}
	])

@app.action("Done")
def endwork(ack , respond):
    ack()
    respond("Have a nice day!")

@app.message("Log_users")
def log(say):
	say("/joke")
	say("logging")
	users = app.client.users_list()
	id = {member["id"] : member["name"] for member in users["members"] if "bot" not in member["name"].lower() }
	for k,v in id.items():
		if log_sql(user_id= k,name = v):
			say(f"Successfully logged {v}")
			global _id
			_id[k] = v
		else:
			say(f"{v} is already logged")
@app.message("Message_users")
def message(say):
	say("Loading...")
	blocks = [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Who do you wish to message?",
				"emoji": True
			}
		},
        {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "all",
						"emoji": True
					},
					"value": "all",
                    "style": "primary",
					"action_id": "Message2"
				}
			]
		}
	]
	try:
		global _id
		for k,v in _id.items():
			blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": v,
                            "emoji": True
                        },
                        "value": k,
                        "style": "primary",
                        "action_id": "Message2"
                    }
                ]
            })
		say(blocks = blocks)
	except Exception as e:
		#implement logging next time
		print(e)
		say("No users logged!")

@app.action("Message2")
def message2(action,ack,client,body):
	ack()
	val = action["value"]
	client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Secret Gratitude Box"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "my_block",
                    "element": {"type": "plain_text_input", "action_id": val},
                    "label": {"type": "plain_text", "text": "What are you greatful to them for?"},
                }
            ],
        },
    )

@app.view("view_1")
def Message3(ack , body):
	ack()
	k,v = list(body["view"]["state"]["values"]["my_block"].items())[0]
	v = v["value"]
	if v == "all":
		for i , _ in _id:
			app.client.chat_postMessage(channel = i  ,text = k )
	else:
		app.client.chat_postMessage(channel = k ,text = v )
@app.event("message")
def handle_message_events():
    pass

def log_sql(user_id = None ,name = None ):
	conn = sqlite3.connect(os.path.join("Slack","users.db"))
	c = conn.cursor()
	if user_id == None or name == None:
		return False
	#check if have users
	c.execute("SELECT * FROM user where user_id=?",(user_id, ))  
	results = c.fetchall()
	if len(results) == 0:   
		c.execute("INSERT INTO user (user_id,username)VALUES( ?,	? )", (user_id,name))
		conn.commit()   
		return True
	else:   
		return False 
	


if __name__ == "__main__":
		c = sqlite3.connect(os.path.join("Slack","users.db")).cursor()
		c.execute("SELECT * FROM user")
		z = c.fetchall()
		for k , v in z:
			_id[k] = v
		handler = SocketModeHandler(app, code)
		handler.start()

