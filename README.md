# music-recommender

``` python
recommender = Recommender()

recommender.artists = [
    'Johnny Cash'
]
recommender.genres = [
    'country',
    'party'
]
recommender.limit = 50

recommendations = recommender.find_recommendations()

for recommendation in recommendations['tracks']:
    print("%s - %s" % (recommendation['album']['name'], recommendation['album']['artists'][0]['name']))

```