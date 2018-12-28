from django.conf.urls import url
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.contrib.gis.geos import Point

from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from haystack.query import SearchQuerySet
from haystack.models import SearchResult

from users.models import Contributor
from projects.models import Project
from ideas.models import Idea

import operator
import functools


class POIResource(Resource):
    r""" City resource for the API
    """

    class Meta:
        include_resource_uri = False
        resource_name = 'poi'
        paginator_class = Paginator

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)" % self._meta.resource_name +
                r"%s$" % trailing_slash(), self.wrap_view('get_search_poi'),
                name="api_get_search_poi"),
        ]

    @classmethod
    def get_models_to_query(cls, request):
        skills = bool(request.GET.get('skills', "true") == "true")
        ideas = bool(request.GET.get('ideas', "true") == "true")
        projects = bool(request.GET.get('projects', "true") == "true")

        models_to_query = []
        if skills:
            models_to_query.append(Contributor)
        if ideas:
            models_to_query.append(Idea)
        if projects:
            models_to_query.append(Project)

        return models_to_query

    def get_search_poi(self, request, **kwargs):
        r""" Returns city around a defined location """

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        models_to_query = self.get_models_to_query(request)
        search = request.GET.get('search', '')

        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        page = (offset / limit) + 1

        # Do the query.
        user_loc = None
        if "lat" in request.GET and "lon" in request.GET:
            if request.GET["lat"] and request.GET["lon"]:
                user_lat = float(request.GET['lat'])
                user_lon = float(request.GET['lon'])
                user_loc = Point(user_lon, user_lat)

        boundaries = None
        if (("bl_lat" in request.GET) and ("bl_lon" in request.GET)
                and ("tr_lat" in request.GET) and ("tr_lon" in request.GET)):
            if (request.GET["bl_lat"] and request.GET["bl_lon"]
                    and request.GET["tr_lat"] and request.GET["tr_lon"]):
                blat = float(request.GET['bl_lat'])
                blon = float(request.GET['bl_lon'])
                tlat = float(request.GET['tr_lat'])
                tlon = float(request.GET['tr_lon'])
                boundaries = (Point(blon, blat), Point(tlon, tlat))
                # limit = None

        if boundaries or user_loc:
            sqs = SearchQuerySet().models(*models_to_query)
            if boundaries:
                sqs = sqs.within('location_poi', *boundaries)
            if user_loc:
                sqs = sqs.distance(
                    'location_poi', user_loc
                ).order_by('distance')
        else:
            sqs = functools.reduce(operator.add, [
                list(model_to_query.split_search(search))
                for model_to_query in models_to_query
            ])

        paginator = Paginator(sqs, limit)

        try:
            page = paginator.page(int(request.GET.get('page', page)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        if not offset:
            offset = (page.number - 1) * limit

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'meta': {
                'limit': limit,
                'next': page.has_next(),
                'previous': page.has_previous(),
                'total_count': page.paginator.count,
                'offset': offset
            },
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def get_object_list(self, request):
        return super(POIResource, self).get_object_list(request)

    def dehydrate(self, bundle):

        # from haystack queryset
        if bundle.obj.__class__ is SearchResult:
            poi_object = bundle.obj.object

        # from classic django queryset
        else:
            poi_object = bundle.obj

        bundle.data['id'] = poi_object.id
        bundle.data['tags'] = poi_object.get_tags()
        bundle.data['title'] = poi_object.get_title()
        bundle.data['subtitle'] = poi_object.get_subtitle()
        bundle.data['latitude'] = poi_object.get_latitude()
        bundle.data['longitude'] = poi_object.get_longitude()
        bundle.data['icon'] = poi_object.get_icon()
        bundle.data['url'] = poi_object.get_absolute_url()

        return bundle

