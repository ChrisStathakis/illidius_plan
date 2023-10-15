from django.db import models
from django.shortcuts import reverse
from .validators import validate_image
from tinymce.models import HTMLField

from .managers import ProjectManager

# Create your models here.


class ProjectCategory(models.Model):
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class ImageProductManager(models.Manager):
    def active(self):
        return super(ImageProductManager, self).filter(active=True)

    def post_related_and_active(self, post):
        return super(ImageProductManager, self).filter(active=True, project_related=post)

    def post_related(self, post):
        return super(ImageProductManager, self).filter(project_related=post)


class Projects(models.Model):
    active = models.BooleanField(default=True)
    show_first_page = models.BooleanField(default=False)
    title = models.CharField(max_length=255, )
    short_description = models.CharField(max_length=255, help_text='The text appears on homepage')
    description = HTMLField()
    seo_description = models.CharField(max_length=255, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    image = models.ImageField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    day_added = models.DateField(auto_now_add=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    demo = models.BooleanField(default=False)
    my_query = ProjectManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Project'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def additional_images_active(self):
        return ImageProject.my_query.post_related_and_active(post=self)

    def additional_images(self):
        return ImageProject.my_query.post_related(post=self)

    def tag_demo(self):
        return 'Demo Site' if self.demo else 'Site'

    def get_absolute_url(self):
        return reverse('product_detail_view', kwargs={'slug': self.slug})

    def tag_image(self):
        return self.image.url


class ImageProject(models.Model):
    primary = models.BooleanField(default=False)
    title = models.CharField(max_length=60)
    alt = models.CharField(max_length=60, null=True, blank=True)
    image = models.ImageField(validators=[validate_image, ])
    text = models.TextField(blank=True, null=True, verbose_name='Optional description.')
    project_related = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="images")
    active = models.BooleanField(default=True)
    objects = models.Manager()
    my_query = ImageProductManager()

    def save(self, *args, **kwargs):
        is_primary = self.primary
        if is_primary:
            ImageProject.objects.filter(primary=True).exlude(id=id).update(primary=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.db import models

# Create your models here.
