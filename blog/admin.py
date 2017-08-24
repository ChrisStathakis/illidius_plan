from django.contrib import admin
from .models import Post, PostCategory, Gallery, PostTags
from mptt.admin import DraggableMPTTAdmin
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['publish', 'updated']
    list_display = ['title', 'active', 'category', 'update']
    list_filter = ['active', 'category', 'update']
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
            'fields': (('active', 'active_eng', 'update'),
                      ('title', 'keywords', 'description'),
                      ('title_eng', 'keywords_eng', 'description_eng'),
                      ('content', 'content_eng'),

                       )
        }),
        ('Εικόνες', {
            'fields': ('file',
                       ('user', 'category'),
                       ('slug', 'likes', 'publish', 'updated'))
        }),
    )


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['image_tiny_tag', 'title', 'url_ready']
    readonly_fields = ['image_tiny_tag', 'url_ready']

admin.site.register(PostCategory, DraggableMPTTAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(PostTags)