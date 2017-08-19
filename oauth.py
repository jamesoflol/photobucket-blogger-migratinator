import requests
import json
import sys

# Usage:
# >>> from oauth import Oauth
# >>> oauth = Oauth('4/4qqg8hwer9ghwiughweruihg')
# >>> print(oauth.access_token)
# >>> oauth.refresh_access_token()
# >>> print(oauth.access_token)
class Oauth:
	__url = "https://www.googleapis.com/oauth2/v4/token"
	__client_id = "475469684563-3tkh3bscomb3548fq4fs8fg7b5t34qlf.apps.googleusercontent.com"
	__client_secret = "ZqObmB0zmVmnv2X8g9F1bojF"
	__redirect_uri = "https://jamesoflol.github.io/photobucket-blogger-migratinator/auth_success"

	def __init__(self, auth_code):
		# get initial auth token from auth code
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
			}
		params = {
			"code": auth_code,
			"client_id": self.__client_id,
			"client_secret": self.__client_secret,
			"redirect_uri": self.__redirect_uri,
			"grant_type": "authorization_code"
			}

		try:
			r = requests.post(self.__url, headers=headers, data=params)
			r.raise_for_status()
		except requests.exceptions.HTTPError as err:
			if err.response.status_code == 400:
				print("ERROR: Are you sure you copied the authorisation code fully, and that you haven't tried to use it more than once?")
				print("Exiting")
				sys.exit(1)
			else:
				raise
		auth_response = json.loads(r.text)
		# e.g., print(auth_response['access_token']) = 1/fFAGRNJru1FTz70BzhT3Zg

		self.__refresh_token = auth_response['refresh_token']
		self.access_token = auth_response['access_token']


	# get new access token from refresh token
	def refresh_access_token(self):
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
			}
		params = {
			"refresh_token": self.__refresh_token,
			"client_id": self.__client_id,
			"client_secret": self.__client_secret,
			"grant_type": "refresh_token"
			}
		r = requests.post(self.__url, headers=headers, data=params)
		r.raise_for_status()
		refresh_response = json.loads(r.text)

		self.access_token = refresh_response['access_token']

		return self

