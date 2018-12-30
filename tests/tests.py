import unittest

from recommender.api import Recommender


class RecommenderTests(unittest.TestCase):

    def test_available_genre_seeds(self):
        recommender = Recommender()
        available_genre_seeds = recommender.available_genre_seeds()
        self.assertIsNotNone(available_genre_seeds)
        self.assertIn('genres', available_genre_seeds)

    def test_find_recommendations(self):
        recommender = Recommender()
        recommender.artists = 'Johnny Cash'
        recommender.genres = [
            'country',
            'party'
        ]
        recommender.track_attributes = {
            'max_danceability': 1.0
        }
        recommender.limit = 10
        recommender.market = 'IE'
        recommendations = recommender.find_recommendations()
        self.assertIsNotNone(recommendations)
        self.assertIn('tracks', recommendations)
        first = recommendations['tracks'][0]
        self.assertIn('name', first)
        self.assertIn('artists', first)
