from django.contrib import admin
from app.models import BlogPost, Tag

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Tag)