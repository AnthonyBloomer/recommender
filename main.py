from recommender.api import Recommender

if __name__ == '__main__':
    recommender = Recommender()
    recommender.artists = 'Johnny Cash'
    recommender.genres = [
        'country',
        'party'
    ]
    recommender.tunable_track_attributes = {
        'danceability': 1.0
    }

    recommendations = recommender.find_recommendations()
    for recommendation in recommendations['tracks']:
        print("%s - %s" % (recommendation['album']['name'], recommendation['album']['artists'][0]['name']))
