import requests
import base64
import six
import os


class ClientCredentialsFlow(object):
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id=None, client_secret=None):

        if not client_id:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')

        if not client_secret:
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise Exception('A client ID and client secret is required.')

        self.client_id = client_id
        self.client_secret = client_secret

        self.token_info = None

    def _make_authorization_header(self):
        auth_header = base64.b64encode(six.text_type(self.client_id + ':' + self.client_secret).encode('ascii'))
        return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    def get_access_token(self):
        payload = {'grant_type': 'client_credentials'}
        headers = self._make_authorization_header()
        response = requests.post(self.OAUTH_TOKEN_URL, data=payload, headers=headers, verify=True)
        if response.status_code != 200:
            raise Exception(response.reason)
        token_info = response.json()
        return token_info['access_token']
