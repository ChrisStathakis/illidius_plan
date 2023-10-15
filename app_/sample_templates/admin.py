from django.contrib import admin
from .models import Category, TemplateSample


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]


@admin.register(TemplateSample)
class TemplateSampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'active']
    list_filter = ['category', 'active']
    fields = ['active', 'title', 'image', 'url', 'category', 'notes', 'free_option', 'price']

