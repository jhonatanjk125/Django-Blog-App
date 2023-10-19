from django.contrib import admin
from app.models import BlogPost, Tag, Comment, Subscriber

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscriber)