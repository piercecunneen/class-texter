from twilio.rest import TwilioRestClient
from dbfunction import verify_number, remove_number
from class_search_web_scrapping import GetClassesHashed
from time import sleep
import sqlite3 as lite
import os


DB_PATH = "/Users/piercecunneen/Documents/NDreviews/class_texter/text_alerts.sqlite"
def Check_for_openings():
	conn = lite.connect(DB_PATH)
	with conn:
		subject_memory = {}
		c = conn.cursor()
		query = "Select * From textAlerts Where verified = 1"
		c.execute(query)
		a = c.fetchall()
		Departments = []

		if a is not None:
			for row in a:
				subject = row[3]
				if subject not in Departments:
					Departments.append(subject)
		courses = GetClassesHashed("201620", Departments, "A", "0ANY", "UG", "M")

		if a is not None:
			for row in a:
				crn = row[0]
				number = row[1]
				subject = row[3]
				course = courses[str(crn)]
				if int(course['Opn']) > 0:
					Send_Open_Spot_text(number, course)
					new_query = "Delete from textAlerts where crn = " + str(crn) + " and number = '" + str(number) + "' and verified = " + str(row[2])
					c.execute(new_query)
def Send_Reply_verification(phone_number = None):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	#messages = client.messages.list(from_ = phone_number).reverse() # Reversed to respond to the earliest messages first
	messages = client.messages.list(from_ = phone_number)

	did_receive = False
	if messages is not None:
		for message in messages:
			body = message.body.lower().strip()
			if body == "accept":
				verify_number(phone_number)
			 	client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been verified! We will send you a message if a spot opens up in your course")
			elif body == "deny":
				remove_number(phone_number)
				client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been disconnected. You will no longer receive messages unless you resign up!")
				message_text = message.body.lower()				#client.messages.delete(message.sid)
			else:
				client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="We cannot understand your response. Please reply 'accept' if you'd like to receive a text alert if a spot opens in your selected course, or 'deny' if you'd like to no longer receive messages")

			message_text = message.body.lower()
			did_receive = True
			try:
			    client.messages.delete(message.sid)
			except:
				pass
	if did_receive:
		return message_text
	else:
		return "No message received"


def Send_Reply_Inquiry(phone_number = None):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	try:
		client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for signing up! To verify, Please reply 'accept' if you'd like to receive a text alert if a spot opens in your selected course, or 'deny' if you'd like to no longer receive messages")
		return 1
	except:
		return 0

def Send_Open_Spot_text(phone_number, course):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')


	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	try:
		client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Attention!!!! " + course["Title"] + " ( "+ course["Course - Sec"] + " ) at " + course["When"] + " now has " + course["Opn"] + " openings! CRN = " + course["CRN"])
		client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="There may have been others watching this class. If it fills up again before you can sign up, you will need to re-sign up for watching this class at NDreviews.com")
	except:
		print "Invalid phone Number"

def Check_For_Responses():
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	messages = client.messages.list()
	for message in messages:
		if message.from_ != TWILIO_NUMBER and message.direction == 'inbound':
			Send_Reply_verification(message.from_)

