from contextlib import nullcontext
from os import name
from django.db import models
from django.utils.text import slugify
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    post_slug = models.SlugField(max_length=200, unique=True)
    post_img = models.ImageField(null=True, blank=True, upload_to="images/")

