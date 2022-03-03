code = "xapp-1-A034FAQDDDM-3211596654640-c330c96fe769612199f661333160576a4ffb25144b6c111c0843ce377b90a193"
token = "xoxb-3165462542083-3165963183010-vSr1qhQ4K8erc1zzPooe7gRQ"
import datetime
import os
import copy
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.flask import SlackRequestHandler
import json
import sqlite3
from flask import Flask , request
import util
#import psycopg2

#conn= psycopg2.connect(
#    host = 'ec2-34-231-183-74.compute-1.amazonaws.com',
#    database = 'dc0igpc5jm4k89',
#    user = 'nfzzdkpylmukuc',
#    password = '7ba6c5d8cb4fde597dd536de44d73f1d6dcfd285ad011e17c5980e0a377a0f67',
#    port = '5432'
#)
#c = conn.cursor()

#create a function that increments the day_ghost in results if not completed and a 
#biweekly function that incrases the weeknum of all in botuser table and push notification to our users

# for results table if weeknum and weeknum of user function is different then do not increment days_ghost
#maybe can add into a did not finish table

_id = {}
app = App(token = token)
with open(os.path.join("jsons", "task_modal.json"), "r") as f:
	task_modal =json.load(f)
with open(os.path.join("jsons", "quiz_modal.json"), "r") as f:
	quiz_modal = json.load(f)
with open(os.path.join("jsons", "task_start.json"), "r") as f:
	task_start =json.load(f)
with open(os.path.join("jsons", "quiz_start.json"), "r") as f:
	quiz_start =json.load(f)
with open(os.path.join("jsons", "msg_usr.json"), "r") as f:
	msg_usr =json.load(f)
with open(os.path.join("jsons", "add_qns.json"), "r") as f:
	add_qns =json.load(f)
	
@app.event("team_join")
def ask_for_introduction(event, say):
	welcome_channel_id = "C034PA3SNF8"
	user_id = event["user"]
	text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
	say(text=text, channel=welcome_channel_id)
	users = app.client.users_list()
	username = users["members"]["name"] if users["members"]["id"] == user_id else None
	if not util.log_sql(user_id = user_id, name = username):
		print("log new user error")

@app.command("/joke")
def joke(say, client, ack):
	ack()
	with open(os.path.join("databases","content", "jokes.txt"), "r") as f:
		jokes = f.read()
	jokes = jokes.split(",")
	random.shuffle(jokes)
	say(jokes[0])
	time = datetime.datetime.now()+datetime.timedelta(seconds=20)
	
	time = int(time.timestamp())
	client.chat_scheduleMessage(channel="D034FAXCME3",text = "reminder",blocks= quiz_start ,post_at=time)
	result = client.chat_scheduledMessages_list()
        # Print scheduled messages
	for message in result["scheduled_messages"]:
		print(message)

@app.message("app")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
def mention_handler( say):
	say(text = "starting tasks...")
	#not implemented
	# add a sql entry in results table adding user_id, week_num , completed = 0, days_ghost = 0
	# if already has entry set days_ghost back to zero
	#util.log_sql_results
	say(blocks = task_start)

@app.action("reminder")
def reminder(body,action,ack, say,client):
	ack()
	if datetime.datetime.today().weekday() in [4,5,6]:
		say(text = "Alright, i have set a reminder for monday 9:30 AM")
		onDay = lambda date, day: date + datetime.timedelta(days=(day-date.weekday()+7)%7)
		date = onDay(datetime.datetime.now().date(),0)
		print(date+ datetime.timedelta())
	else:
		say(text = "Alright, i have set a reminder for tommorow 9:30 AM")
		date = datetime.date.today() + datetime.timedelta(days=1)
	scheduled_time = datetime.time(hour=9, minute=30)
	time = datetime.datetime.combine(date, scheduled_time).timestamp()
	if action["value"] == "message_1":
		client.chat_scheduleMessage(channel=body['container']['channel_id'],text = "reminder",blocks = task_start,post_at=time)
	else:
		client.chat_scheduleMessage(channel=body['container']['channel_id'],text = "reminder",blocks = quiz_start,post_at=time)
	app.client.chat_delete( channel= body['container']['channel_id'], ts =body['message']['ts'] )


@app.action("task1")
def modal_for_content(body , client , ack ):
	del_msg = f"{body['container']['channel_id']},{body['message']['ts']}"
	print(del_msg)
	ack()
	data = copy.deepcopy(task_modal)
	# not implemented
	#tasks = util.select_sql_tasks_modal(3)
	#for task in tasks:
	#	data["blocks"].append(json.loads(task)) convert it to json 
	data["private_metadata"] = del_msg
	client.views_open(trigger_id=body["trigger_id"],view = data )


@app.action("task_modal_choose")
def task_modal_choose(ack,body,action,client):
	ack()
	#print(body["user"]["id"])
	#print(action["block_id"])
	data = copy.deepcopy(task_modal)	
	for item in data["blocks"]:
		if item.get("block_id", None) == action["block_id"]:
			item["elements"][0]["text"]["text"] = "Choosen:thumbsup:"
			item["elements"][0]["style"] = "primary"
		data["private_metadata"] = body["view"]["private_metadata"]
		#action["block_id"] is the task_name and action["value"] is task_id
		data["blocks"][0]["block_id"]=action["block_id"]+","+action["value"]
	client.views_update(view_id=body["view"]["id"],hash=body["view"]["hash"],view = data)


@app.view("task_modal_view")
def close_task(say,body,ack):
	ack()
	metadata = body["view"]["private_metadata"].split(",")
	task = body["view"]["blocks"][0]["block_id"]
	taskname = task.strip("task_").split(",")
	if len(taskname) != 2:
		say(channel = metadata[0], text ="Please choose a choice by pressing the choose button")
	else:
		metadata = body["view"]["private_metadata"].split(",")
		app.client.chat_delete(channel = metadata[0], ts = metadata[1])
		say(channel = metadata[0], text = taskname[1])
		#add sql call to alter results setting task_id and days_ghost = 0
		#util.log_sql_qns_choice(user_id , task_id)

		#sql call to get task_lesson based on task_id
		#util.select_task_lesson
		say( channel=metadata[0], blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Here is your lesson carefully curated by CyberSierra on {taskname[0]} \n Once you finish your lesson there will be a quiz so please pay attention!:eyes:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Lesson time",
					"emoji": True
				},
				"value": task,
				"style" : "primary",
				#url will change base on the sql call
				"url": "https://www.cybersierra.co/",
				"action_id": "Content_piece"
			}
		}
	])
@app.action("Content_piece")
def check_if_ready(say,action,ack):
	ack()
	task = action["value"]
	data = copy.deepcopy(quiz_start)
	data[1]["elements"][0]["value"] = task
	say(blocks = data)

@app.action("quiz_modal")
def quiz_modal_view(client,action,body,ack):
	ack()
	val = action["value"]
	print(val)
	#taskname = val.strip("task_")
	#place holder before i implment sql
	qns = util.select_sql_qns(1)
	if len(qns) == 0:
		qns.append((1,'{"qns_content": "question context", "qns_qns": "what is the best language", "qns_correct": "python", "qns_wrong1": "java", "qns_wrong2": "c++", "qns_wrong3" :"Golang", "qns_task":"1"}'))
	qn = list(json.loads(qns[0][1]).items())
	#qn = list(qn.items())
	random.shuffle(qn)
	data = copy.deepcopy(quiz_modal)
	print(qn)
	#for ans,result in answers:
	for results , answer in qn:
		if results == "qns_content":
			data["blocks"][0]["text"]["text"] = answer
			continue
		if results == "qns_task":
			#need a way to pass the task_num
			#data["blocks"][2]["block_id"] = answer
			del_msg = f"{body['container']['channel_id']},{body['message']['ts'],{answer}}"
			continue
		if results == "qns_qns":
			data["blocks"][2]["label"]["text"] = answer
			continue	
		data["blocks"][2]["element"]["options"].append({
					"text": {
							"type": "plain_text",
							"text": answer,
						},
						"value": ("true" if results == "qns_correct" else "false")
					})
	data["private_metadata"]=del_msg
	print(data)
	client.views_open(trigger_id=body["trigger_id"], view= data)

@app.view("quiz_modal_view")
def results(body, say, ack):
	ack()
	metadata = body["view"]["private_metadata"].split(",")
	app.client.chat_delete(channel = metadata[0], ts = metadata[1])
	id = body["user"]["id"]
	selected = list(body["view"]["state"]["values"]["quiz_response"].items())
	print(selected)
	option = selected[0][1]['selected_option']['text']['text']
	correct = selected[0][1]['selected_option']["value"]
	print(option)
	temp = {}
	for entry in body["view"]["blocks"][2]["element"]["options"]:
		temp[entry["text"]["text"]] = entry["value"]
		if entry["value"] == "true":
			ans = entry["text"]["text"]
	print(id)
	response = "You got it"+ (" correct!:tada:" if correct == "true" else f" wrong:smiling_face_with_tear: Correct answer was {ans}")
	print(response)
	say(channel = id , text = response)
	say(channel = id ,text = "Thank you for finishing all you task!")
	#maybe add a feed back
	#add sql



@app.command("/starts")
def log(say,ack):
	ack()
	say("logging")
	users = app.client.users_list()
	id = {member["id"] : member["name"] for member in users["members"] if "bot" not in member["name"].lower() }
	for k,v in id.items():
		if util.log_sql(user_id= k,name = v):
			say(f"Successfully logged in {v}")
			global _id
			_id[k] = v
		else:
			say(f"{v} is already logged")

@app.message("Message_users")
def message(say):
	say("Loading...")
	data = copy.deepcopy(msg_usr)
	try:
		_id
		for k,v in _id.items():
			data.append({
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
		say(blocks = data)
	except Exception as e:
		#implement logging next time
		print(e)
		say("No users logged!")

@app.command("/addqns")
def add_questions(ack,client,body):
	ack()
	client.views_open(trigger_id=body["trigger_id"], view = add_qns)

@app.view("addqns")
def log_quetions(body, ack,say):
	ack()
	id = body["user"]["id"]
	qns = {}
	for key ,value in body['view']["state"]["values"].items():
		print(key,value['plain_text_input-action']["value"])
		qns[key] = str(value['plain_text_input-action']["value"])
	if util.log_sql_qns(qns):
		say(channel = id , text = "Successfully added question")
	else:
		say(channel = id , text = "Error, question was not added")

@app.action("Message2")
def message2(action,ack,client,body):
	ack()
	val = action["value"]
	client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "Messaging",
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
        }
    )

@app.view("Messaging")
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

@app.message("radio_button")
def handle_message_events(say):
    say(blocks =  [
		{
			"type": "actions",
			"elements": [
				{
					"type": "radio_buttons",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "*this is plain_text text*",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "*this is plain_text text*",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "*this is plain_text text*",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "actionId-0"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click Me",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "gay"
				}
			]
		}
	])

@app.action("gay")
def temp(ack,body):
	ack()
	print(body)
	

#heroku inplementation	
#flask_app = Flask(__name__)
#handler = SlackRequestHandler(app)
#@flask_app.route("/slack/events", methods=["POST"])
#def slack_events():
#    return handler.handle(request)

if __name__ == "__main__":
	conn = sqlite3.connect(os.path.join("databases","users.db"))
	c = conn.cursor()
	c.execute("SELECT user_id,user_name FROM botusers")
	for k , v in c.fetchall():
		_id[k] = v
	handler = SocketModeHandler(app, code)
	handler.start()

