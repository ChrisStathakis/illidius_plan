from django.db import models


class ImageProductManager(models.Manager):

    def get_active(self):
        return super().queryset