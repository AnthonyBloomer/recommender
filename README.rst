recommender
===========

Python client for the `Spotify Recommendations
API <https://developer.spotify.com/documentation/web-api/reference/browse/get-recommendations/>`__.

Install:

::

   pip install music-recommender

Example:

.. code:: python


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

