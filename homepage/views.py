from django.shortcuts import render, render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import View, FormView, CreateView, DetailView, ListView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.template.context_processors import csrf
from .models import *
from newsletter.forms import Join, JoinForm, JoinFormEng
from blog.models import Post, PostCategory, PostTags, Gallery
from blog.forms import PhotoForm, GalleryForm
from .forms import ContactForm
from projects.models import Projects, ImageProject
from django.views.decorators.cache import cache_page, cache_control


# Create your views here.

WELCOME_PAGE_ID = 1
ABOUT_ID = 1


def my_cookie_law(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie('cookie_law', True)
    return response


def homepage_initial_data(request):
    page_info = get_object_or_404(WelcomePage, id=WELCOME_PAGE_ID)
    about = get_object_or_404(AboutMe, id=ABOUT_ID)
    blog = Post.my_query.return_last_posts()
    projects = Projects.my_query.active()
    get_cookie = request.COOKIES.get('cookie_law', None)
    return [page_info, about, blog, projects, get_cookie]


def about_initial_data():
    about_page_info = AboutPage.objects.filter(active=True).last()
    about_messages = AboutMessages.objects.filter(page_related=about_page_info)
    about_techo = AboutTecho.objects.filter(page_related=about_page_info)
    projects = Projects.my_query.demo_sites()
    return [about_page_info, about_messages, about_techo, projects]


class Homepage(View):
    form_class = JoinForm
    template_name = 'timer/index.html'

    def get(self, request):
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        form = self.form_class
        context = locals()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        context = locals()
        return render(request, self.template_name, context)


class HomePageEng(View):
    form_class = JoinFormEng
    template_name = 'english/index.html'

    def get(self, request):
        form = self.form_class
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for the subscribe!')
            return HttpResponseRedirect('/#call-to-action')
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)


class About(View):
    form_class = JoinFormEng
    template_name = 'timer/about.html'
    
    def get(self, request):
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        about_page_info, about_messages, about_techo, projects = about_initial_data()
        context = locals()
        return render_to_response(self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for the subscribe!')
        context = locals()
        context.update(csrf(request))
        return render_to_response(self.template_name, context)


class AboutEng(View):
    template_name = 'english/about.html'

    def get(self, request):
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        about_page_info, about_messages, about_techo, projects = about_initial_data()
        context = locals()
        return render_to_response(self.template_name, context)


class Service(ListView):
    model = Services
    template_name = 'timer/service.html'

    def get_context_data(self, **kwargs):
        object_list = self.object_list
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        demo_sites = Projects.my_query.demo_sites()
        return locals()


class ServiceEng(ListView):
    model = Services
    template_name = 'english/service.html'

    def get_context_data(self, **kwargs):
        object_list = self.object_list
        page_info = WelcomePage.objects.get(id= WELCOME_PAGE_ID)
        demo_sites = Projects.my_query.demo_sites()
        return locals()


class Works(ListView):
    model = Projects
    template_name = 'timer/gallery.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        page_info = WelcomePage.objects.get(id=1)
        context = locals()
        context.update(super(Works, self).get_context_data())
        return context


class WorksEng(ListView):
    model = Projects
    template_name = 'english/gallery.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        page_info = WelcomePage.objects.get(id=1)
        object_list = self.object_list
        context = locals()
        return context


# @cache_page(60*15)
class BlogPage(ListView):
    model = Post
    template_name = 'timer/blog-left-sidebar.html'

    def get_context_data(self, **kwargs):
        #object_list = self.object_list
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        about_me = AboutMe.objects.get(id=ABOUT_ID)
        post_categories = PostCategory.objects.all()
        updates = self.object_list.filter(update = True)
        post_tag = PostTags.objects.all()
        posts = self.object_list
        context = locals()
        return context

    def get_queryset(self):
        queryset = self.model.my_query.active()
        search_text = self.request.GET.get('search_text')
        queryset = queryset.filter(Q(title__icontains=search_text) | Q(category__title__icontains=search_text) | Q(content__icontains=search_text)).distinct() if search_text else queryset
        cat_name = self.request.GET.getlist('cat_name')
        queryset = queryset.filter(category__id__in=cat_name) if cat_name else queryset
        return queryset


class BlogPageEng(ListView):
    model = Post
    template_name = 'english/blog-left-sidebar.html'

    def get_context_data(self, **kwargs):
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        about_me = AboutMe.objects.get(id=ABOUT_ID)
        post_categories = PostCategory.objects.all()
        updates = self.object_list.filter(update=True)
        post_tag = PostTags.objects.all()
        posts = self.object_list
        search_text = self.request.GET.get('search_text')
        cate_name = self.request.GET.getlist('cat_name')
        context = locals()
        return context

    def get_queryset(self):
        queryset = self.model.my_query.active_and_eng()
        search_text = self.request.GET.get('search_text')
        cate_name = self.request.GET.getlist('cat_name')
        queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
        queryset = queryset.filter(Q(title_eng__icontains=search_text) | Q(category__title__icontains=search_text)).distinct() if search_text else queryset
        return queryset


class PostPage(DetailView):
    model = Post
    template_name = 'timer/single-post.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        object = self.object
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        post_tag = PostTags.objects.all()
        context = locals()
        return context


class PostPageEng(DetailView):
    model = Post
    template_name = 'english/single-post.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        object = self.object
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        post_tag = PostTags.objects.all()
        context = locals()
        return context


class ContactPage(SuccessMessageMixin, CreateView):
    template_name = 'timer/contact.html'
    form_class = ContactForm
    success_url = '/contact'

    def get_context_data(self, **kwargs):
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        context = locals()
        context.update(super(ContactPage, self).get_context_data())
        return context

    def get_success_message(self, cleaned_data):
        return "Σας ευχαριστούμε για την επικοινωνία, θα σας απαντησούμε σύντομα"


class ContactPageEng(SuccessMessageMixin, CreateView):
    template_name = 'english/contact.html'
    form_class = ContactForm
    success_url = '/'

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Thank you!"


class ProjectPage(DetailView):
    model = Projects
    template_name = 'timer/single-portfolio.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        page_info, about, services, projects, cookie_law = homepage_initial_data(self.request)
        context = super(ProjectPage, self).get_context_data(**kwargs)
        context['images'] = ImageProject.my_query.post_related_and_active(post=self.object)
        context['page_info'] = page_info
        return context


class ProjectPageEng(DetailView):
    model = Projects
    template_name = 'english/single-portfolio.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProjectPageEng, self).get_context_data(**kwargs)
        context['images'] = ImageProject.my_query.post_related_and_active(post=self.object)
        return context


class PostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        if user.is_authenticated():
            obj.add_or_remove_likes(user=user)
        return obj.absolute_url()


class PostLikeEng(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        if user.is_authenticated():
            obj.add_or_remove_likes(user=user)
        return obj.absolute_url()


def blog_create(request):
    images = Gallery.objects.all()
    if request.POST:
        form_photo = GalleryForm(request.POST, request.FILES)
        if form_photo.is_valid():
            photo = form_photo.save()
            data = {'is_valid': True,
                    'title': photo.file.title,
                    'url':form_photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        form_photo = GalleryForm()

    if request.POST:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('homepage')
    else:
        form = PhotoForm()

    context = locals()
    return render(request, 'test_templates/create_blog.html', context)


class BasicUploadView(View):
    def get(self, request):
        photos_list = Gallery.objects.all()
        return render(self.request, 'test_templates/index.html', {'photos': photos_list})

    def post(self, request):
        form = GalleryForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def cache_clear(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug,format=None):
        #slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
                liked= False
            else:
                obj.likes.add(user)
                liked = True
            updated= True
        data = {
            'updated':updated,
            'liked':liked,
        }
        return Response(data)
'''