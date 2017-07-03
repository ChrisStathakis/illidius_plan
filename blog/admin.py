from django.contrib import admin
from .models import Post, PostCategory, Gallery, PostTags
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


admin.site.register(PostCategory)
admin.site.register(Gallery)
admin.site.register(PostTags)