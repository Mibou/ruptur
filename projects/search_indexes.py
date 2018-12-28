from haystack import indexes
from .models import Project


class ProjectsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created_at = indexes.DateTimeField(model_attr='created_at')
    location_project = indexes.LocationField(model_attr='get_location')
    location_poi = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Project
