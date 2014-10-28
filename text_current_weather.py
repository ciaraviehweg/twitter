import requests

BASE_URL = 'http://api.wunderground.com/api/7afb6acd16b73b96/conditions/q'

# find the weather URL for a state, city
def weather(state, city):
    city = city.replace(" ", "_")
    return "{}/{}/{}.json".format(BASE_URL, state, city)

# function that finds the current temperature of a state, city
def current_temp(state, city):
	r = requests.get(weather(state, city))
	j = r.json()
	temperature = j['current_observation']['temperature_string']
	return temperature

from twilio.rest import TwilioRestClient

account_sid = "ACcf8f9f34b30047da0ed876e8fb6923e1"
auth_token = "7e30959e79ff5a55b6b85fb470a50957"
client = TwilioRestClient(account_sid, auth_token)

# message = client.messages.create(body="Hi!",
# 	to="+14156025667",
# 	from_="+14158438333")

def text_this(number, message, test = False):
	if test:
		print "This would have sent an SMS to {}. Message: {}".format(number, message)
		return True	

	msg = client.messages.create(to=number, from_="+14158438333", body=message)
	return msg

text_this('4156025667', current_temp("CA", "San Francisco"))
