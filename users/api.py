from tastypie.resources import ModelResource
from .models import Skill


class SkillResource(ModelResource):
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skills'
        excludes = ['email']
        allowed_methods = ['get']
