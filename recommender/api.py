import requests
import logging
import base64
import six
import os


class _ClientCredentialsFlow(object):
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


class Recommender(object):
    def __init__(self, client_id=None, client_secret=None):
        auth = _ClientCredentialsFlow(client_id, client_secret)
        self.token = auth.get_access_token()

        self.url = 'https://api.spotify.com/v1/'

        self._artist_ids = []
        self._track_ids = []
        self._genres = []
        self._limit = 20
        self._track_attributes = {}
        self._market = ""

        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }

        self._available_genre_seeds = None

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("music-recommender")

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        if limit > 100:
            self.logger.warning("Maximum target size is 100.")
        self._limit = limit

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, market):
        self._market = market

    @property
    def track_attributes(self):
        return self._track_attributes

    @track_attributes.setter
    def track_attributes(self, track_attributes):
        self._track_attributes = track_attributes

    def available_genre_seeds(self):
        if self._available_genre_seeds is None:
            self._available_genre_seeds = self._make_request('recommendations/available-genre-seeds', params=None)
        return self._available_genre_seeds

    def _is_genre_seed_available(self, genre):
        if self._available_genre_seeds is None:
            self._available_genre_seeds = self.available_genre_seeds()
        return genre in self._available_genre_seeds['genres']

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres):
        if isinstance(genres, list):
            for genre in genres:
                genre = genre.lower()
                if self._is_genre_seed_available(genre):
                    self._genres.append(genre)
        else:
            genres = genres.lower()
            if self._is_genre_seed_available(genres):
                self._genres.append(genres)
        if not self._genres:
            self.logger.warning("No matching seeds found for given genre.")

    @property
    def artists(self):
        return self._artist_ids

    @artists.setter
    def artists(self, artists):
        self._artist_ids = []
        if isinstance(artists, list):
            for artist in artists:
                artist = self._lookup_artist_id(artist)
                if artist:
                    self._artist_ids.append(artist)
        else:
            artist = self._lookup_artist_id(artists)
            if artist:
                self._artist_ids.append(artist)
        if not self._artist_ids:
            self.logger.warning("No matching seeds found for given artist.")

    @property
    def tracks(self):
        return self._track_ids

    @tracks.setter
    def tracks(self, tracks):
        self._track_ids = []
        if isinstance(tracks, list):
            for track in tracks:
                self._track_ids.append(self._lookup_track_id(track))
        else:
            self._track_ids.append(self._lookup_track_id(tracks))
        if not self._track_ids:
            self.logger.warning("No matching seeds found for given track.")

    def find_recommendations(self):
        if not self._artist_ids and not self.genres and not self.tracks:
            raise Exception("At least one artist, genre, or track seed is required.")
        params = {
            'seed_artists': self._artist_ids,
            'seed_genres': self.genres,
            'seed_tracks': self.tracks,
            'limit': self.limit
        }
        params.update(self.track_attributes)
        recs = self._make_request(endpoint='recommendations', params=params)
        return recs

    def _lookup(self, term, lookup_type):
        params = {
            'q': term,
            'type': lookup_type
        }
        return self._make_request(endpoint='search', params=params)

    def _lookup_track_id(self, track):
        tracks = self._lookup(term=track, lookup_type='track')

        if len(tracks['tracks']['items']):
            return tracks['tracks']['items'][0]['id']

        self.logger.warning("No results found for: %s" % track)

    def _lookup_artist_id(self, artist_name):
        artists = self._lookup(term=artist_name, lookup_type='artist')

        if len(artists['artists']['items']):
            return artists['artists']['items'][0]['id']

        self.logger.warning("No results found for: %s" % artist_name)

    def _make_request(self, endpoint, params):
        response = requests.get(self.url + endpoint, params=params, headers=self.headers)
        if response.status_code != 200:
            self.logger.error(response.content)
            raise Exception(response.reason)
        json = response.json()
        return json
