from django.shortcuts import render
from .forms import CommentForm
from .models import BlogPost, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    posts = BlogPost.objects.all()
    top_posts = BlogPost.objects.all().order_by('-view_count')[0:3]
    recent_posts = BlogPost.objects.all().order_by('-last_updated')[0:3]
    context = {'posts':posts, 'top_posts':top_posts, 'recent_posts':recent_posts}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = BlogPost.objects.get(post_slug = slug)
    comments = Comment.objects.filter(post=post, parent=None)
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
            parent_object = None
            #Check if our post request has a parent value to save as a reply.
            if request.POST.get('parent'):
                #Save a reply
                parent = request.POST.get('parent')
                parent_object = Comment.objects.get(id=parent)
                if parent_object:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_object
                    comment_reply.post = post
                    comment_reply.save()
            else:
                #Save a comment
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
            return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    return render(request, 'app/post.html', context)
