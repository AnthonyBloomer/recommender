from recommender.api import Recommender

recommender = Recommender()
recommender.artists = 'Johnny Cash'
recommender.genres = [
    'country',
    'party'
]
recommender.track_attributes = {
    'danceability': 1.0
}

recommendations = recommender.find_recommendations()
for recommendation in recommendations['tracks']:
    print("%s - %s" % (recommendation['name'], recommendation['artists'][0]['name']))