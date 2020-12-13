from django.urls import path
from .views import ShowCaseListView, ShowCaseDetailView


app_name = 'showcase'

urlpatterns = [
    path('list/', ShowCaseListView.as_view(), name='list'),

    ]