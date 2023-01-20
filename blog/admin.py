from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'date_updated', 'author']
    prepopulated_fields = {'slug': ('title', 'author',)}
