from django.views.generic import TemplateView, ListView, DetailView


class HomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        pass


class AboutView(TemplateView):
    template_name = "about.html"


