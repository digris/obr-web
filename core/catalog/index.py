from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Artist


@register(Artist)
class ArtistIndex(AlgoliaIndex):
    custom_objectID = "uid"
    # fields = ('name', 'date')
    # geo_field = 'location'
    # settings = {'searchableAttributes': ['name']}
    index_name = "artist_index"
