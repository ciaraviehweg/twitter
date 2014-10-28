import requests

BASE_URL = 'http://api.wunderground.com/api/7afb6acd16b73b96/forecast/q'

# find the weather URL for a state, city
def weather(state, city):
    city = city.replace(" ", "_")
    return "{}/{}/{}.json".format(BASE_URL, state, city)

# a function that finds a 3 day forecast of a given state, city
def forecast(state, city):
	r = requests.get(weather(state, city))
	j = r.json()
	forecast = j['forecast']['txt_forecast']['forecastday']
	for day in forecast:
		print day['title'], day['fcttext_metric']


from twilio.rest import TwilioRestClient

account_sid = "ACcf8f9f34b30047da0ed876e8fb6923e1"
auth_token = "7e30959e79ff5a55b6b85fb470a50957"
client = TwilioRestClient(account_sid, auth_token)

def text_this(number, message, test=False):
	if test:
		print "This would have sent an SMS to {}. Message: {}".format(number, message)
		return True	

	msg = client.messages.create(to=number, from_="+14158438333", body=message)
	return msg

text_this('+14156025667', forecast("CA", "San Francisco"))


