from django.conf.urls import url
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage

from tastypie.resources import Resource
from tastypie.utils import trailing_slash

from haystack.query import SearchQuerySet
from haystack.utils.geo import Point

from users.models import Contributor
from projects.models import Project
from ideas.models import Idea


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

    def get_search_poi(self, request, **kwargs):
        r""" Returns city around a defined location """

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        skills = bool(request.GET.get('skills', "true") == "true")
        ideas = bool(request.GET.get('ideas', "true") == "true")
        projects = bool(request.GET.get('projects', "true") == "true")
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

        # Temporarily disabled
        # if boundaries or user_loc:
        if False:
            sqs = SearchQuerySet().models(
                Contributor, Idea, Project
            )
            if boundaries:
                sqs = sqs.within('location', *boundaries)
            if user_loc:
                sqs = sqs.distance(
                    'location', user_loc
                ).order_by('distance')
        else:
            sqs = (
                list(Idea.split_search(search) if ideas else []) +
                list(Contributor.split_search(search) if skills else []) +
                list(Project.split_search(search) if projects else [])
            )

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
        bundle.data['id'] = bundle.obj.id
        bundle.data['tags'] = bundle.obj.get_tags()
        bundle.data['title'] = bundle.obj.get_title()
        bundle.data['subtitle'] = bundle.obj.get_subtitle()
        bundle.data['latitude'] = bundle.obj.get_latitude()
        bundle.data['longitude'] = bundle.obj.get_longitude()
        bundle.data['icon'] = bundle.obj.get_icon()
        bundle.data['url'] = bundle.obj.get_absolute_url()
        return bundle
