from django.db import models

from tinymce.models import HTMLField

CATEGORIES = (
    ('a', 'Website'),
    ('b', 'Αφορα Επιχειρισεις'),
    ('c', 'Λοιπά')
)


def upload_location(instance, filename):
    return f'showcase/{instance.title}/{filename}'


class ShowCase(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    site_related = models.URLField(blank=True)
    text = HTMLField(blank=True)
    image = models.ImageField(upload_to=upload_location)
    category = models.CharField(max_length=1, choices=CATEGORIES)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def str(self):
        return self.title

