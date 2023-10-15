from django.views.generic import ListView

from .models import Category, TemplateSample


class TemplateListView(ListView):
    template_name = 'sample/list-view.html'
    model = TemplateSample
    paginate_by = 20

    def get_queryset(self):
        qs = TemplateSample.filters_data(self.request)
        return qs

    def get_context_data(self, **kwargs):
        context = super(TemplateListView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update(locals())
        return context