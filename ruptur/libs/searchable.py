from django.db import models


class Searchable(models.Model):
    def search():
        pass

    class Meta:
        abstract = True
