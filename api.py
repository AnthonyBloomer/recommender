import requests
import logging
from auth import ClientCredentialsFlow


class Recommender(object):
    def __init__(self, client_id=None, client_secret=None):
        """
        https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/
        :param client_id
        :param client_secret
        """
        auth = ClientCredentialsFlow(client_id, client_secret)
        self.token = auth.get_access_token()

        self.url = 'https://api.spotify.com/v1/'

        self._artist_ids = []
        self._track_ids = []
        self._genres = []
        self._limit = 20
        self._tunable_track_attributes = {}
        self._market = ""

        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }

        self._available_genre_seeds = None

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("music-recommender")

    def available_seed_genres(self):
        if self._available_genre_seeds is None:
            self._available_genre_seeds = self._make_request('recommendations/available-genre-seeds', params=None)
        return self._available_genre_seeds

    def _is_genre_seed_available(self, genre):
        if self._available_genre_seeds is None:
            self._available_genre_seeds = self.available_seed_genres()
        return genre in self._available_genre_seeds['genres']

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, market):
        self._market = market

    @property
    def tunable_track_attributes(self):
        return self._tunable_track_attributes

    @tunable_track_attributes.setter
    def tunable_track_attributes(self, tunable_track_attributes):
        self._tunable_track_attributes = tunable_track_attributes

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
                genre = genre.lower()
                if self._is_genre_seed_available(genre):
                    self._genres.append(genre)
        else:
            genres = genres.lower()
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
                artist = self._lookup_artist_id(artist)
                if artist:
                    self._artist_ids.append(artist)
        else:
            artist = self._lookup_artist_id(artists)
            if artist:
                self._artist_ids.append(artist)

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
        else:
            self.logger.warning("No results found for: %s" % track)

    def _lookup_artist_id(self, artist_name):
        artists = self._lookup(term=artist_name, lookup_type='artist')
        if len(artists['artists']['items']):
            return artists['artists']['items'][0]['id']
        else:
            self.logger.warning("No results found for: %s" % artist_name)

    def find_recommendations(self):
        if not self._artist_ids and not self.genres and not self.tracks:
            raise Exception("At least one artist, genre, or track is required.")
        params = {
            'seed_artists': self._artist_ids,
            'seed_genres': self.genres,
            'seed_tracks': self.tracks,
            'limit': self.limit
        }
        params.update(self.tunable_track_attributes)
        recs = self._make_request(endpoint='recommendations', params=params)
        return recs

    def _make_request(self, endpoint, params):
        response = requests.get(self.url + endpoint, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.reason)
        json = response.json()
        return json
    
    
