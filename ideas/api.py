from tastypie.resources import ModelResource
from tastypie import fields
from .models import Idea, Vote, Contribution
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization


class IdeaResource(ModelResource):
    class Meta:
        authentication = SessionAuthentication()
        authorization = Authorization()
        queryset = Idea.objects.all()
        allowed_methods = ['get']

    def hydrate(self, bundle):
        bundle.obj.creator = bundle.request.user.contributor
        return bundle


class ContributionResource(ModelResource):
    idea = fields.ForeignKey(IdeaResource, 'idea')

    class Meta:
        authentication = SessionAuthentication()
        authorization = Authorization()
        queryset = Contribution.objects.all()
        allowed_methods = ['get']

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle


class VoteResource(ModelResource):
    idea = fields.ForeignKey(IdeaResource, 'idea')

    class Meta:
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = Authorization()
        queryset = Vote.objects.all()
        allowed_methods = ['post', 'get']

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

    def full_dehydrate(self, bundle):
        bundle.data['up'] = bundle.obj.idea.get_votes_up().count()
        bundle.data['down'] = bundle.obj.idea.get_votes_down().count()
        return bundle
