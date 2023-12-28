from django.contrib import admin
from blogs.models import Blog

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    search_fields = ['id', 'title', 'content']

admin.site.register(Blog, BlogAdmin)