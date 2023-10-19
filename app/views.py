from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def home(request):
    posts = BlogPost.objects.all()
    context = {'posts':posts}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = BlogPost.objects.get(post_slug = slug)
    context = {'post':post}
    return render(request, 'app/post.html', context)
