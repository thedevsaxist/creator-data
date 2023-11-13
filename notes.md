**Consumer key**: is the API key that a service provider (Twitter, Facebook, etc.) issues to a consumer (a service that wants to access a user's resources on the service provider). This key is what identifies the consumer.

**Consumer secret**: is the consumer "password" that is used, along with the consumer key, to request access (i.e. authorization) to a user's resources from a service provider.

**Access token**: is what is issued to the consumer by the service provider once the consumer completes authorization. This token defines the access privileges of the consumer over a particular user's resources. Each time the consumer wants to access the user's data from that service provider, the consumer includes the access token in the API request to the service provider.

## Steps to using Oauth
### 1. Consumer Token and Consumer Token Secrets:

Get the `consumer key` (this is like the username for the developer account) and the `consumer secrets` (this is like the password for the developer account).
```py
# this generates the request token
request_token = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token)
    print(fetch_response)
except ValueError:
    (
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print(f"Got OAuth token: {resource_owner_key}")
```

### 2. Access Token and Access Token Secrets

Get authorization using the oauth consumer tokens and secrets. The access token gives the level of authorization needed to access some certain data form the API. This is done using the `access token` and the `access token secret`.

```py
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
```

### 3. Make your requests using the Access Token and Access Token Secrets

Finally, all you need to do now is to make your request to the API using the access token and the access token secrets when necessary. 