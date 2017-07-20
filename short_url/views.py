from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.views import View

from .models import *
from .forms import *
# Create your views here.


class ShortHomepage(View):
    template = 'short_url/home.html'
    def get(self, request, *args, **kwargs):
        #ShortingURL.objects.all().delete()
        form = ShortURLForm()
        context = locals()
        return render(request, self.template, context)
    def post(self, request, *args, **kwargs):
        if request.POST:
            print(request.POST)
            form = ShortURLForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data.get('url')
                costumer_code = form.cleaned_data.get('costumer_code')
                new_url = ShortingURL.objects.get_or_create(url=url, costumer_code=costumer_code) if costumer_code else ShortingURL.objects.get_or_create(url=url)
                new_url = new_url.save()
                get_url = 'http://127.0.0.1:8000/s/%s/' % new_url.shortcode
                messages.success(request, '%s' % get_url)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context = locals()
        return render(request, self.template, context)

def redirect_view(request, slug):
    get_url = get_object_or_404(ShortingURL, shortcode=slug)
    return HttpResponseRedirect(get_url.url)


