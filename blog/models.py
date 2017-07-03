from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
# Create your models here.


def post_upload(instance, filename):
    return 'post/%s/%s' % (instance.title, filename)

def gallery_upload(instance, filename):
    return 'gallery/%s/%s' % (instance.title, filename)

class PostTags(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class PostCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    content = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.title

    def count_posts(self):
        counts = Post.objects.filter(category=self).count() if Post.objects.filter(category=self) else 0
        return counts

class Post(models.Model):
    active = models.BooleanField(default=True)
    active_eng = models.BooleanField(default=True)
    title = models.CharField(max_length=100, unique=True, verbose_name='Title')
    content = models.TextField(verbose_name='Content', help_text='Use Html!!!')
    keywords = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    title_eng = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title ENG')
    content_eng = models.TextField(verbose_name='Content_eng', help_text='Use Html!!!', blank=True, null=True)
    keywords_eng = models.CharField(max_length=100, blank=True, null=True)
    description_eng = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='user')
    publish = models.DateField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True,null=True, blank=True, allow_unicode=True, verbose_name='Slug - Dont bother with that ')
    category = models.ForeignKey(PostCategory, null=True)
    file = models.ImageField(verbose_name='Image', help_text='1332*550')
    update = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')

    def __str__(self):
        return self.title

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def absolute_url(self):
        return reverse('blog_page', kwargs={'slug':self.slug})

    def get_absolute_url(self):
        return reverse('blog_page', kwargs={'slug':self.slug})

    def api_absolute_url(self):
        return reverse('api_like', kwargs={'slug':self.slug})

    def add_or_remove_likes(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)
        self.save()

class Gallery(models.Model):
    title = models.CharField(default='Gallery', max_length=30)
    image = models.ImageField(upload_to=gallery_upload)

    def __str__(self):
        return self.title