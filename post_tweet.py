# pip install requests
# pip install requests-oauthlib

# API secrets. NEVER share these with anyone!
CLIENT_KEY = "xjhjANI0aQEkG41pv2VOBwmy0"
CLIENT_SECRET = "PKDLnxG0VTnN88VwGBjE8lgbJEIBNCRKSQ90Vscjb2k59UcDnN"


API_URL = "https://api.twitter.com"
REQUEST_TOKEN_URL = API_URL + "/oauth/request_token"
AUTHORIZE_URL = API_URL + "/oauth/authorize?oauth_token={request_token}"
ACCESS_TOKEN_URL = API_URL + "/oauth/access_token"
TIMELINE_URL = API_URL + "/1.1/statuses/home_timeline.json"
USER_URL = API_URL + "/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2"
MY_URL = API_URL + "/1.1/statuses/user_timeline.json?screen_name=shaciarasf&count=10"
MENTIONS_URL = API_URL + "/1.1/statuses/mentions_timeline.json?count=2&since_id=14927799"
MYMENTIONS_URL = API_URL + "/1.1/statuses/mentions_timeline.json?count=2&since_id=525337588396089344"
USERID_URL = API_URL + "/1.1/mutes/users/ids.json?cursor=-1"

SEARCH_URL = API_URL + "/1.1/search/tweets.json?q=%22What%27s%20the%20weather%22"

TWEET_URL = API_URL + "/1.1/statuses/update.json"



import urlparse
import json
import requests
from requests_oauthlib import OAuth1


def get_request_token():
    """ Get a token allowing us to request user authorization """
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET)
    response = requests.post(REQUEST_TOKEN_URL,
                             auth=oauth)
    credentials = urlparse.parse_qs(response.content)

    request_token = credentials.get("oauth_token")[0]
    request_secret = credentials.get("oauth_token_secret")[0]
    return request_token, request_secret


def get_access_token(request_token, request_secret, verifier):
    """"
    Get a token which will allow us to make requests to the API
    """
    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=request_token,
                   resource_owner_secret=request_secret,
                   verifier=verifier)

    response = requests.post(ACCESS_TOKEN_URL, auth=oauth)
    credentials = urlparse.parse_qs(response.content)
    access_token = credentials.get('oauth_token')[0]
    access_secret = credentials.get('oauth_token_secret')[0]
    return access_token, access_secret


def get_user_authorization(request_token):
    """
    Redirect the user to authorize the client, and get them to give us the
    verification code.
    """
    authorize_url = AUTHORIZE_URL
    authorize_url = authorize_url.format(request_token=request_token)
    print 'Please go here and authorize: ' + authorize_url
    return raw_input('Please input the verifier: ')


def store_credentials(access_token, access_secret):
    """ Save our access credentials in a json file """
    with open("access.json", "w") as f:
        json.dump({"access_token": access_token,
                   "access_secret": access_secret}, f)


def get_stored_credentials():
    """ Try to retrieve stored access credentials from a json file """
    with open("access.json", "r") as f:
        credentials = json.load(f)
        return credentials["access_token"], credentials["access_secret"]


def authorize():
    """ A complete OAuth authentication flow """
    try:
        access_token, access_secret = get_stored_credentials()
    except IOError:
        request_token, request_secret = get_request_token()
        verifier = get_user_authorization(request_token)
        access_token, access_secret = get_access_token(request_token,
                                                       request_secret,
                                                       verifier)
        store_credentials(access_token, access_secret)

    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=access_token,
                   resource_owner_secret=access_secret)
    return oauth


def main():
    """ Main function """
    auth = authorize()

    response = requests.get(SEARCH_URL, auth=auth)    
    # print json.dumps(response.json(), indent=4)
    make_tweet("test", auth)        

def make_tweet(status_message, auth):
    data = { 'status': status_message }
    response = requests.post(TWEET_URL, data=data, auth=auth)
    print json.dumps(response.json(), indent=4)







if __name__=="__main__":main()











