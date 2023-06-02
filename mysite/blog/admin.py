from django.contrib import admin
from .models import Post

# Register your models here.

# admin.site.register(Post)


# We are telling the Django administration site that the model is registered in the site using a custom
# class that inherits from ModelAdmin. In this class, we can include information about how to display
# the model on the site and how to interact with it.
# The list_display attribute allows you to set the fields of your model that you want to display on the
# administration object list page. The @admin.register() decorator performs the same function as the
# admin.site.register() function that you replaced, registering the ModelAdmin class that it decorates.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']

    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
