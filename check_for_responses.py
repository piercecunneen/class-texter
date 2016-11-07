from Get_messages import Check_for_openings
import os

Check_for_openings()



# from twilio.rest import TwilioRestClient
# ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
# AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
# TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')
# print "acct_sid = {}\n".format(ACCOUNT_SID)
# print "auth_token = {}\n".format(AUTH_TOKEN)

# account_sid = "{{ account_sid }}" # Your Account SID from www.twilio.com/console
# auth_token  = "{{ auth_token }}"  # Your Auth Token from www.twilio.com/console

# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# message = client.messages.create(body="Hello from Python",
#     to="+16109522515",    # Replace with your phone number
#     from_=TWILIO_NUMBER) # Replace with your Twilio number

# print(message.sid)
