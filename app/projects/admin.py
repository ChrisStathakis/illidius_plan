from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


def action_deactive_first_page(modeladmin, request, queryset):
    queryset.update(show_first_page=False)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'show_first_page']
    list_filter = ['active',]
    actions = [action_deactive_first_page, ]
    fieldsets = (
        ('Greek', {
            'fields': (('active', 'demo'),
                       ('show_first_page', 'short_description'),
                       ('title', 'seo_description', 'seo_keywords'),
                       'description'
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

@admin.register(ProjectCategory)
class ProjectCategoyAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Projects, ProjectAdmin)
admin.site.register(ImageProject, ImageProjectAdmin)

