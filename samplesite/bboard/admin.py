from django.contrib import admin

from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published', 'category')
    list_display_links = ('title', 'content')
    search_fields =  ('title', 'content', )
    


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
