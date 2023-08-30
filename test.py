import pathlib

from requests.auth import HTTPBasicAuth

print()
import requests
CLIENT_ID = 'ATNkERSn02NVfTmsVuhwb0V7pYG2dyxG9ZqiDD60zmSQbDyoEsQ6CAtg0ExbYXlDarx2gJ0vKp1TkhfF'
CLIENT_SECRET = 'ECZNkYnjpVER4HzGW4Da-vUJD5IFNhz0YoZagIxF4hsve_6vtS7wLfzoAOv7MVhMHodVx9peQYhBWOUE'
def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'GRANT-TYPE': 'client_credentials'
    }
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', {
        'GRANT-TYPE': 'CLIENT_CREDENTIALS'
    }, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET), headers=headers)
    print(response.json())

print(get_access_token())
client_id = '<the id you get from github>'
client_secret = '<the secret you get from github>'

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

from requests_oauthlib import OAuth2Session
github = OAuth2Session(CLIENT_ID)

# Redirect user to GitHub for authorization
authorization_url, state = github.authorization_url()
print ('Please go here and authorize,', authorization_url)

# Fetch a protected resource, i.e. user profile
r = github.get('https://api.github.com/user')
print (r.content)
