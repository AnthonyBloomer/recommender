# recommender

Python client for the [Spotify Recommendations API](https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/). 

Install:

```
pip install music-recommender
```

Example:

``` python

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

```
