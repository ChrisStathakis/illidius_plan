from django.urls import path

from .views import ticker_homepage_api_view, TickerListApiView, TickerUpdateApiView

app_name = 'api_tickers'

urlpatterns = [
    path('', ticker_homepage_api_view, name='home'),
    path('ticker/list/', TickerListApiView.as_view(), name='ticker_list'),
    path('ticker/update/<int:pk>/', TickerUpdateApiView.as_view(), name='ticker_update'),


]