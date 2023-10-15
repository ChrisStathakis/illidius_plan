from django.contrib import admin

from .models import ShowCase


@admin.register(ShowCase)
class ShowCaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price',  'active']
