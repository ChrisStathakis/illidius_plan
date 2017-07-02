from django.contrib import admin
from .models import *
# Register your models here.



class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active', 'active_eng']
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields':(('active', 'active_eng', 'demo'),
                      ('title', 'seo_description', 'seo_keywords'),
                      ('title_eng', 'seo_description_eng', 'seo_keywords_eng'),
                      )
        }),
        ('Page Info',{
            'fields':(('image', 'category'),
                      ('description', 'description_eng'),
                      'href'
                      )
        }),
        ('Seo',{'classes': ('collapse',),
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
