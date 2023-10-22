from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


# Create your models here.

class Author(models.Model):
    """Author class, it has a one to one relationship with users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.user.first_name

class Subscriber(models.Model):
    """To store information about users who subscribe using the main page"""
    email = models.EmailField(max_length=100)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.email


class Tag(models.Model):
    """Handles tags information and their relations to posts"""
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name

    
class BlogPost(models.Model):
    """Post class, includes relations to the title, content, image, author, bookmarks, and likes."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    post_slug = models.SlugField(max_length=200, unique=True)
    post_img = models.ImageField(null=True, blank=True, upload_to='images/', storage=S3Boto3Storage())
    tags = models.ManyToManyField(Tag, blank=True, related_name='blogpost')
    view_count = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bookmarks = models.ManyToManyField(User, related_name='booksmarks', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', default=None, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Used to store comments and replies"""
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.name} on {self.post} - email: {self.email}'

class WebsiteMeta(models.Model):
    """Used to store website meta so that information can be changed using the admin panel"""
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    about = models.TextField()