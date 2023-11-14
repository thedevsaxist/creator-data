import json
from requests_oauthlib import OAuth1Session
import os
from dotenv import load_dotenv

load_dotenv()

# this adds our API_key and secrets to the environment variable
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRETS')

# consumer_key = "DbzPC6h5VLiBu89BEHkibfBMC"
# consumer_secret = "uTWlhfXp8DPTGpGEQicR9BgHbIuBimwhTnz2WHtRN7zAFrVxRc"


# these are optional parameters that we are passing into the endpoint
fields = "created_at,description, name, pinned_tweet_id, username, verified"
params = {"user.fields": fields}


# this generates the request token
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
    print(fetch_response)
except ValueError:
    print(
        "!!!!!!!!!!!!!!!!!!\nThere may have been an issue with the consumer_key or consumer_secret you entered.\n"
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print(f"Got OAuth token: {resource_owner_key}")

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print(f"Please go here and authorize: {authorization_url}")
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret
)

# this is the endpoint we are trying to access
request_url = "https://api.twitter.com/2/users/me"
response = oauth.get(request_url, params=params)

if response.status_code != 200:
    raise Exception(
        f"Request returned as error {response.status_code} {response.text}"
    )

print(f"Request returned {response.status_code}")

json_response = response.json()

print(json.dumps(json_response, indent=4, sort_keys=True))


#TODO: Debug this to find out why you're getting a 401 error