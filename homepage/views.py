from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.views.generic import View, FormView, CreateView, DetailView, ListView, RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from .models import *
from newsletter.forms import Join, JoinForm
from blog.models import Post, PostCategory, PostTags
from .forms import ContactForm
from projects.models import Projects, ImageProject
from django.views.decorators.cache import cache_page
# Create your views here.

WELCOME_PAGE_ID = 1
ABOUT_ID = 1

def homepage_initial_data():
    page_info = get_object_or_404(WelcomePage, id=WELCOME_PAGE_ID)
    about = get_object_or_404(AboutMe, id=ABOUT_ID)
    services = Services.objects.all()
    projects = Projects.my_query.active()
    return [page_info, about, services, projects]

def about_initial_data():
    about_page_info = AboutPage.objects.filter(active=True).last()
    about_messages = AboutMessages.objects.filter(page_related=about_page_info)
    about_techo = AboutTecho.objects.filter(page_related=about_page_info)
    about_clients = AboutClients.objects.filter(page_related=about_page_info)
    return [about_page_info, about_messages, about_techo, about_clients]

class Homepage(View):
    def get(self, request):
        page_info, about, services, projects = homepage_initial_data()
        context = locals()
        return render_to_response('timer/index.html', context)

class HomePageEng(View):
    def get(self, request):
        page_info, about, services, projects = homepage_initial_data()
        context = locals()
        return render_to_response('english/index.html', context)


class About(View):
    def get(self, request):
        page_info, about, services, projects = homepage_initial_data()
        about_page_info, about_messages, about_techo, about_clients = about_initial_data()
        context = locals()
        return render_to_response('timer/about.html', context)

class AboutEng(View):
    def get(self, request):
        page_info, about, services, projects = homepage_initial_data()
        about_page_info, about_messages, about_techo, about_clients = about_initial_data()
        context = locals()
        return render_to_response('english/about.html', context)


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
        queryset = Post.objects.filter(active=True)
        search_text = self.request.GET.get('search_text')
        queryset = queryset.filter(Q(title__icontains=search_text) | Q(category__title__icontains=search_text) | Q(content__icontains=search_text)).distinct() if search_text else queryset
        cat_name = self.request.GET.getlist('cat_name')
        queryset = queryset.filter(category__id__in=cat_name) if cat_name else queryset
        return queryset

class BlogPageEng(ListView):
    model = Post
    template_name = 'english/blog-left-sidebar.html'
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
    template_name = 'timer/single-post.html'
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
        page_info, about, services, projects = homepage_initial_data()
        context = locals()
        context.update(super(ContactPage, self).get_context_data())
        return context

    def get_success_message(self, cleaned_data):
        return "Σας ευχαριστούμε για την επικοινωνία, θα σας απαντησούμε σύντομα"

class ContactPageEng(SuccessMessageMixin, CreateView):
    template_name = 'timer/contact.html'
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
        page_info, about, services, projects = homepage_initial_data()
        context = super(ProjectPage, self).get_context_data(**kwargs)
        context['images'] = ImageProject.my_query.post_related_and_active(post=self.object)
        context['page_info'] = page_info
        return context

class ProjectPageEng(DetailView):
    model = Projects
    template_name = 'timer/single-portfolio.html'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super(ProjectPageEng, self).get_context_data(**kwargs)
        context['images'] = ImageProject.my_query.post_related_and_active(post=self.object)
        print(context['images'])
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


from blog.forms import PhotoForm
def blog_create(request):
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