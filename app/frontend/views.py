from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from projects.models import Projects, ProjectCategory
from contact.forms import Contact, ContactForm


class HomepageView(FormView):
    template_name = "index.html"
    form_class = ContactForm
    success_url = reverse_lazy("homepage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Homepage"
        context["projects"] = Projects.my_query.first_page()
        return context

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, "Thank you for the message")
        return super().form_valid(form)


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


