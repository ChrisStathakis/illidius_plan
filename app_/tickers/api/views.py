from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404


from django_filters.rest_framework import DjangoFilterBackend


from .serializers import (TickerSerializer, )
from ..models import Ticker


@api_view(['GET'])
def ticker_homepage_api_view(request, format=None):
    return Response({
        'tickers': reverse('api_tickers:ticker_list', request=request, format=format),

    })


class TickerListApiView(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'ticker']


class TickerUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    permission_classes = [AllowAny, ]
