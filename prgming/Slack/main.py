code = "xapp-1-A034FAQDDDM-3168440167236-e2f1e3734c3311e88ba448bd0e4187a34f89a48137174e767b968e45b6c0c557"
token = "xoxb-3165462542083-3165963183010-EArtapJ8aizdSqJJy5Ebkxux"


from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

jokes = set(["//be nice to the CPU\nThread_sleep(1);" , "!false\n(It's funny because it's true.)" ,"What did the router say to the doctor?\n'It hurts when IP'","Nidhish"])

app = App(token = token)

@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "#test"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)

app.client.conversations_open

@app.message("joke")
def joke(say):
    say(jokes.pop())


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
    say("logging")
    chatId = app.client.conversations_list(types= "im")
    global _id
    _id = set([entry["id"] for entry in chatId["channels"]])

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
        for i in _id:
            blocks.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": i,
                            "emoji": True
                        },
                        "value": i,
                        "style": "primary",
                        "action_id": "Message2"
                    }
                ]
            })
    except Exception as e:
        #implement logging next time
        print("error" , e)
    say(blocks = blocks)

@app.action("Message2")
def message2(action,ack,respond):
    ack()
    respond("sending")
    val = action["value"]
    if val == "all":
        for i in _id:
            app.client.conversations_open(channel=i)
            app.client.chat_postMessage(channel=i,text = "bot here, nid is a joke")
    else:
        app.client.conversations_open(channel=val)
        app.client.chat_postMessage(channel=val,text = "hello nid is a joke")

@app.event("message")
def handle_message_events():
    pass


if __name__ == "__main__":
        handler = SocketModeHandler(app, code)
        handler.start()
