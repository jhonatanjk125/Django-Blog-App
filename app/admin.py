from django.contrib import admin
from app.models import BlogPost, Tag, Comment, Subscriber, Author, WebsiteMeta

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(Author)
admin.site.register(WebsiteMeta)