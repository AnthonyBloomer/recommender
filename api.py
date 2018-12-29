import requests
from auth import ClientCredentialsFlow


class Recommender(object):
    def __init__(self, client_id=None, client_secret=None):
        auth = ClientCredentialsFlow(client_id, client_secret)
        self.token = auth.get_access_token()

        self.url = 'https://api.spotify.com/v1/'

        self._artist_ids = []
        self._track_ids = []
        self._genres = []
        self._limit = 20

        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }

        self._available_genre_seeds = None

    def _is_genre_seed_available(self, genre):
        if self._available_genre_seeds is None:
            self._available_genre_seeds = self._make_request('recommendations/available-genre-seeds', params=None)
        return genre in self._available_genre_seeds['genres']

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        self._limit = limit

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres):
        if isinstance(genres, list):
            for genre in genres:
                if self._is_genre_seed_available(genre):
                    self._genres.append(genre)
        else:
            if self._is_genre_seed_available(genres):
                self._genres.append(genres)
        if not self._genres:
            raise Exception("No matching seeds found for given genre.")

    @property
    def artists(self):
        return self._artist_ids

    @artists.setter
    def artists(self, artists):
        self._artist_ids = []
        if isinstance(artists, list):
            for artist in artists:
                self._artist_ids.append(self._lookup_artist_id(artist))
        else:
            self._artist_ids.append(self._lookup_artist_id(artists))

    @property
    def tracks(self):
        return self._track_ids

    @tracks.setter
    def tracks(self, tracks):
        self._artist_ids = []
        if isinstance(tracks, list):
            for track in tracks:
                self._track_ids.append(self._lookup_track_id(track))
        else:
            self._track_ids.append(self._lookup_track_id(tracks))

    def _lookup_track_id(self, track):
        params = {
            'q': track,
            'type': 'track'
        }
        json = self._make_request(endpoint='search', params=params)
        return json['tracks']['items'][0]['id']

    def _lookup_artist_id(self, artist_name):
        params = {
            'q': artist_name,
            'type': 'artist'
        }
        json = self._make_request(endpoint='search', params=params)
        return json['artists']['items'][0]['id']

    def find_recommendations(self):
        params = {
            'seed_artists': self._artist_ids,
            'seed_genres': self.genres,
            'seed_tracks': self.tracks,
            'limit': self.limit
        }
        recs = self._make_request(endpoint='recommendations', params=params)
        return recs

    def _make_request(self, endpoint, params):
        response = requests.get(self.url + endpoint, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.reason)
        json = response.json()
        return json

