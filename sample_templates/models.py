from django.db import models
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError

MAX_SIZE_FILE = 1024*1024/2
MEDIA_URL = ''


def validate_image_size(value):
    if value.file.size > MAX_SIZE_FILE:
        return ValidationError('το αρχείο είναι μεγαλύτερο από 0.5 mb')


def upload_image_location(instance, filename):
    return f'products/{instance.id}/{filename}'


class Category(models.Model):
    title = models.CharField(unique=True, max_length=240)

    def __str__(self):
        return self.title


class TemplateSample(models.Model):
    active = models.BooleanField(default=True)
    url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    notes = HTMLField(blank=True)
    image = models.ImageField(blank=True,
                              upload_to=upload_image_location,
                              help_text='400*400',
                              validators=[validate_image_size, ]
                              )
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    free_option = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @staticmethod
    def filters_data(request):
        all_templates = TemplateSample.objects.filter(active=True)
        categories = request.GET.getlist('cate_name', None)
        all_templates = all_templates.filter(category__in=categories) if categories else all_templates
        return all_templates
