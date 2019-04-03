from django.contrib import admin
from .models import *
# Register your models here.


def action_deactive_first_page(modeladmin, request, queryset):
    queryset.update(show_first_page=False)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'show_first_page']
    list_filter = ['active', 'active_eng']
    actions = [action_deactive_first_page, ]
    fieldsets = (
        ('Greek', {
            'fields': (('active', 'demo'),
                       ('show_first_page', 'short_description'),
                       ('title', 'seo_description', 'seo_keywords'),
                       'description'
                       )
        }),
        ('English', {
            'fields': (('active_eng', 'short_description_eng'),
                       ('title_eng', 'seo_description_eng', 'seo_keywords_eng'),
                       'description_eng'
                       )
        }),
        ('Page Info', {
            'fields': (('image', 'category'),
                       ('href', 'github'),
                       )
        }),
        ('Seo', {'classes': ('collapse',),
                 'fields': ('slug', ),
        }),
    )


class ImageProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'alt', 'project_related', 'active', ]
    list_filter = ['project_related', 'active']
    fieldsets = (
        ('Photo Info',{
            'fields':(('title', 'alt', 'active'),'project_related','image', 'text')
        }),
    )


admin.site.register(Projects, ProjectAdmin)
admin.site.register(ImageProject, ImageProjectAdmin)
admin.site.register(ProjectCategory)
