from django.contrib import admin
from .models import (
    MemberCompany
)


@admin.register(MemberCompany)
class MemberCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', )
    search_fields = ['name', 'domain']
