from django.contrib import sitemaps
from django.urls import reverse
from projects.models import Projects


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['homepage_eng', 'about_eng',
                'gallery_eng', 'blog_eng', 'gym_page', 'shorting_url']

    def location(self, obj):
        return reverse(obj)


class ProjectSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return Projects.my_query.active()