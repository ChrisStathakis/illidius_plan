from django.db import models


class PostManager(models.Manager):

    def get_active(self):
        return super().get_queryset().filter(active=True)

    def get_return_last_posts(self):
        return self.get_active().order_by("id")[:6]

