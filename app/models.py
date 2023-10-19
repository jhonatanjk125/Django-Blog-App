from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name

    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    post_slug = models.SlugField(max_length=200, unique=True)
    post_img = models.ImageField(null=True, blank=True, upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True, related_name='blogpost')
    view_count = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.name} on {self.post} - email: {self.email}'