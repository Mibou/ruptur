from haystack import indexes
from .models import Idea


class IdeasIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created_at = indexes.DateTimeField(model_attr='created_at')
    location_idea = indexes.LocationField(model_attr='get_location')
    location_poi = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Idea
