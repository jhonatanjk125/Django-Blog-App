from django.shortcuts import render
from .forms import CommentForm
from .models import BlogPost, Comment

# Create your views here.
def home(request):
    posts = BlogPost.objects.all()
    context = {'posts':posts}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = BlogPost.objects.get(post_slug = slug)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()
    context = {'post':post, 'form':form, 'comments':comments}
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

    return render(request, 'app/post.html', context)
