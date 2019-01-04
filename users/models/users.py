from django.contrib.auth.models import AbstractUser

__all__ = [
    'User'
]


class User(AbstractUser):
    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()
