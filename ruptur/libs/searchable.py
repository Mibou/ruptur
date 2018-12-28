from django.db import models


class Searchable(models.Model):

    @classmethod
    def search(cls, match):
        pass

    @classmethod
    def split_search(cls, match):
        result = None
        clean_match = match.strip()

        if not clean_match:
            return cls.objects.all()

        for split in clean_match.split(' '):
            if not split:
                continue

            if not result:
                result = cls.search(split)
                continue

            result &= cls.search(split)

        return result

    class Meta:
        abstract = True
