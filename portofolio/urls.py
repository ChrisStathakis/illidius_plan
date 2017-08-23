"""portofolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from homepage.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView
from newsletter.views import subscribe
from blog.views import *
from short_url.views import *

sitemaps = {
    'blog': BlogSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Homepage.as_view(), name='homepage'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^service/$', Service.as_view(), name='service'),
    url(r'^works/$', Works.as_view(), name='gallery'),
    url(r'^blog/$', cache_page(60*2)(BlogPage.as_view()), name='blog'),
    url(r'^blog/(?P<slug>[-\w]+)/$', cache_page(60*2)(PostPage.as_view()), name='blog_page'),
    url(r'^contact/$', ContactPage.as_view(), name='contact'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectPage.as_view(), name='project_page'),
    #english
    url(r'^en/$', HomePageEng.as_view(), name='homepage_eng'),
    url(r'^en/about/$', AboutEng.as_view(), name='about_eng'),
    url(r'^en/service/$', ServiceEng.as_view(), name='service_eng'),
    url(r'^en/works/$', WorksEng.as_view(), name='gallery_eng'),
    url(r'^en/blog/$', BlogPageEng.as_view(), name='blog_eng'),
    url(r'^en/blog/(?P<slug>[-\w]+)/$', PostPageEng.as_view(), name='blog_page_eng'),
    url(r'^en/contact/$', ContactPageEng.as_view(), name='contact_eng'),
    url(r'^en/project/(?P<slug>[-\w]+)/$', ProjectPageEng.as_view(), name='project_page_eng'),
    url(r'^subscribe/$', view=subscribe, name='subscribe'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^sitemap\.xml',sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', include('robots.urls')),
    #test_urls

    url(r'^create_blog/$', view=blog_create, name='create_blog'),
    url(r'^basic-upload/$', BasicUploadView.as_view(), name='basic_upload'),
    url(r'^like/(?P<slug>[-\w]+)/$', PostLike.as_view(), name='like'),
    url(r'^cache-clear/$', view=cache_clear, name='cache_clear'),
    #url(r'^api/like/(?P<slug>[-\w]+)/$', PostLikeApi.as_view(), name='api_like'),

    #short_code module
    url(r'^shorting-url/$', ShortHomepage.as_view(), name='shorting_url'),
    url(r'^s/(?P<slug>[-\w]+)/$', view=redirect_view, name='redirect_result'),

    url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

