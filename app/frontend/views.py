from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        pass


