from django.db import models


class ImageProductManager(models.Manager):

    def get_active(self):
        return super().get_queryset().filter(active=True)


class ProjectManager(models.Manager):

    def get_active(self):
        return super().get_queryset().filter(active=True)

    def demo_sites(self):
        return self.get_active().filter(demo=True)

    def first_page(self):
        return self.get_active().filter(show_first_page=True)