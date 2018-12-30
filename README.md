# Music Recommendation API

This is a Python client for the [Spotify Recommendations API](https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/). 

>Recommendations are generated based on the available information for a given seed entity and matched against similar artists and tracks. If there is sufficient information about the provided seeds, a list of tracks will be returned together with pool size details.

Example:

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
