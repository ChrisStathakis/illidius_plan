from django.contrib.sitemaps import Sitemap
from django.views.generic import ListView
from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = ""

    def get_queryset(self):
        return Post.my_query.get_active()

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(active=True)
