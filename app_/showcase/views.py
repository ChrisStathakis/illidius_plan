from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import ShowCase


class ShowCaseListView(ListView):
    model = ShowCase
    template_name = 'showcase/list.html'
    queryset = ShowCase.objects.filter(active=True)


class ShowCaseDetailView(DetailView):
    model = ShowCase
    queryset = ShowCase.objects.filter(active=True)
    template_name = ''


