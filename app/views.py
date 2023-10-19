from django.shortcuts import render
from .forms import CommentForm
from .models import BlogPost

# Create your views here.
def home(request):
    posts = BlogPost.objects.all()
    context = {'posts':posts}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = BlogPost.objects.get(post_slug = slug)
    form = CommentForm()
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()
    context = {'post':post, 'form':form}
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = BlogPost.objects.get(id = post_id)
            comment.post = post
            comment.save()

    return render(request, 'app/post.html', context)
