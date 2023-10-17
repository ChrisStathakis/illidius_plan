from django.views.generic import TemplateView, ListView, DetailView

from projects.models import Projects, ProjectCategory


class HomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Homepage"
        context["projects"] = Projects.my_query.first_page()
        return context


class AboutView(TemplateView):
    template_name = "about.html"


class ProjectListView(ListView):
    model = Projects
    queryset = Projects.my_query.get_active()
    template_name = "projects.html"

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        context["page_title"] = "Projects"
        return context


class ProductDetailView(DetailView):
    model = Projects
    queryset = Projects.my_query.get_active()
    template_name = ""
    slug_field = "slug"


