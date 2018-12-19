from flask import Flask, request
from transitions.extensions import GraphMachine
import requests
import os
#import pygraphviz
import pymongo
import ssl

from fsm import *
from joke_fact_generator import *

MANGODB_PASS = os.environ.get('MANGODB_PASSWORD')
MANGODB_USER = os.environ.get('MANGODB_USERNAME')


myClient = pymongo.MongoClient(f"mongodb://{MANGODB_USERNAME}:{MANGODB_PASS}B@mapdata-shard-00-00-hmafm.mongodb.net:27017,mapdata-shard-00-01-hmafm.mongodb.net:27017,mapdata-shard-00-02-hmafm.mongodb.net:27017/test?ssl=true&replicaSet=MapData-shard-0&authSource=admin&retryWrites=true")
db = myClient['tainan']
myCol = db['Interesting spots']

# for x in myCol.find():
# 	print(x)



VERIFY_TOKEN = os.environ.get('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'

app = Flask(__name__)

state_machine = StateMachine(states = states, transitions = transitions, initial = 'init')
FunMaker = FunGenerator(0, 0)
#state_machine.get_graph().draw('my_graph.png', prog = 'dot')
@app.route('/', methods=['GET'])
def verify():
	mode = request.args.get("hub.mode")
	token = request.args.get("hub.verify_token")
	challenge = request.args.get("hub.challenge")

	if mode == "subscribe" and token == VERIFY_TOKEN:
		print("WEBHOOK VERIFIED")
		return challenge

@app.route('/', methods=['POST'])
def webhook_handler():
	data = request.get_json()
	print(data)
	reply_routine()
	return f"this should return {data}",200


def parsed_user_message(msg):
	#state_machine.get_graph().draw('my_graph.png', prog = 'dot') 
	# A number of lists which contain key words that the bot uses to interpret users responses
	start_over = ['start again', 'restart', 'try again', 'begin again', 'retry', 'one more time']
	greetings = ['hi', 'hello', 'greetings', 'hey', 'yo', 'hey there']
	greetings_suffix = [' botty', '!', '.', ' :)']
	joke_init = ['joke', 'funny', 'humor', 'laugh']
	fun_fact_init = ['interesting', 'fact', 'fun fact', 'trivia', 'knowledge', 'know']
	init_init = ['start', 'over', 'start over', 'try again', 'restart']
	request_init = ['find', 'fun', 'place', 'go to', 'hang out', 'relax', 'chill', 'looking for', 'search', 'searching', 'look for']
	request_choice_history = ['history', 'historic site', 'historic']
	request_choice_park = ['park', 'parks', 'nature', 'fresh air', 'forest', 'meadow', 'woodland']
	request_choice_museum = ['museum', 'museums']
	choice_none = ['none', 'None', 'none of the above', 'neither', 'none of these', 'none of them', 'another', 'changed my mind', 'choose another', 'other']
	# Reply to a greeting
	for pre in greetings:
		for suf in greetings_suffix:
				greet = pre + suf
				if msg == pre or msg == greet:
					if state_machine.state == 'init':
						return 'Hi there! What can I do for you?' 
					else:
						return 'Well...Hello again!'
				else:
					continue

	# Get back to init state from any other state
	if any(word in msg.lower() for word in init_init):
		state_machine.goto_init()
		print(state_machine.state)
		return "Okay let's start over! Hi I am Botty! :) \n\nI can tell you a joke, a fun fact, or find an interesting place to go to!"
	
	if state_machine.state == 'init' or state_machine.state == 'joke' or state_machine.state == 'fun_fact':
		if any(word in msg.lower() for word in joke_init):
			# Tell a joke
			# Source states: init, joke, fun_fact
			# Dest states: init, joke, fun_fact, request
			state_machine.make_joke()
			return FunMaker.tell_joke()
		elif any(word in msg.lower() for word in fun_fact_init):
			# Give a fact
			# Source states: init, joke, fun_fact
			# Dest states: init, joke, fun_fact, request
			state_machine.give_fact()
			return FunMaker.tell_fact()
		elif any(word in msg.lower() for word in request_init):
			# Process a request
			# Source states: joke, fun_fact, init
			# Dest states: request
			state_machine.request()
			return "Okay! Would you prefer to go to a park, a museum, or a historic site?"
		else:
			return "Sorry, I didn't quite get that..."

	# Here the user chooses whether they prefer a park/museum/historic site
	if state_machine.state == 'request':
		if any(word in msg.lower() for word in request_choice_history):
			state_machine.history_choice()
			return database_query("historic_site")
		elif any(word in msg.lower() for word in request_choice_park):
			state_machine.park_choice()
			return database_query("park")
		elif any(word in msg.lower() for word in request_choice_museum):
			state_machine.museum_choice()
			return database_query("museum")
		else:
			return "Please choose one of the categories!"

	# Check which place user prefers (if any)
	if state_machine.state == 'satisfy_check':
		choice = myCol.find_one({'name': msg})
		if any(word in msg.lower() for word in choice_none):
			state_machine.not_satisfied()
			return 'Okay lets try again, Would you prefer to go to a park, a museum, or a historic site?'
		if choice:
			state_machine.satisfied()
			return 'Sounds good! Here is the address:\n' + choice['address'] + '\n\nAnd the link to the map:\n' + choice['map_link'] + '\nHave fun!'
		else:
			return "Hmm...sorry I didn't get that, can you please type the exact name?"

	return 'What do you mean by: ' + msg

def database_query(category):
	choiceNum = myCol.count_documents({'category': category})
	loopCnt = 1
	print(choiceNum)

	queryReply = 'I have a couple of choices for you...which one would you prefer?\n\n'

	# Iterate through the database looking for the category which the user selected
	for place in myCol.find({'category': category}):
		queryReply += place['name']
		if loopCnt < choiceNum:
			queryReply += ', '
		if loopCnt == choiceNum-1:
			queryReply += 'or '
		loopCnt+=1
	queryReply+= '\nWhich one would you like to go to?'
	return queryReply

def send_msg(recipient_id, send_text, imageUrl):
	
	if imageUrl != '':
		payload = {
			'message': {
				'attachment': {
					'type': 'image',
					'payload': {
						'url': imageUrl,
					}
				}
			},
			'recipient': {
				'id': recipient_id
			},
			'notification_type' : 'regular'
		}
	else:
		payload = {
		'message': {
			'text': send_text,
		},
		'recipient': {
			'id': recipient_id
		},
		'notification_type' : 'regular'
	}

	authorize = {
		'access_token': PAGE_ACCESS_TOKEN
	}

	response = requests.post(FB_API_URL, params = authorize, json = payload)

	if response.status_code != 200:
		print("\nUnable to send the message :(\n\n" + response.text)
	return response

def initiate_response(recipient_id, recv_text):
	response = parsed_user_message(recv_text)
	# Send images of the 3 places of choice (parks/museums/historic sites).
	# Only occurs while we are choosing a specific place from one of the states (parks/museums/historic sites).
	if state_machine.state == 'parks':
		state_machine.satisfy_check()
		send_msg(recipient_id, response, '')
		# Search the database where the 'category' field matches what user selects
		for place in myCol.find({'category': 'park'}):
			send_msg(recipient_id, response, place['photo'])
	elif state_machine.state == 'museums':
		state_machine.satisfy_check()
		send_msg(recipient_id, response, '')
		for place in myCol.find({'category': 'museum'}):
			send_msg(recipient_id, response, place['photo'])
	elif state_machine.state == 'historic_sites':
		state_machine.satisfy_check()
		send_msg(recipient_id, response, '')
		for place in myCol.find({'category': 'historic_site'}):
			send_msg(recipient_id, response, place['photo'])
	else:
		send_msg(recipient_id, response, '')


def reply_routine():
	payload = request.get_json()
	collection = payload['entry'][0]['messaging']
	print(state_machine.state)

	for msg in collection:
		if (msg.get('message') and msg['message'].get('text')):
			text = msg['message']['text']
			sender_id = msg['sender']['id']
			initiate_response(sender_id, text)
	return "OK", 200
