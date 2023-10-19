from django.shortcuts import render
from .forms import CommentForm, SubscriberForm
from .models import BlogPost, Comment, Tag
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    posts = BlogPost.objects.all()
    top_posts = BlogPost.objects.all().order_by('-view_count')[0:3]
    recent_posts = BlogPost.objects.all().order_by('-last_updated')[0:3]
    featured_posts = BlogPost.objects.filter(is_featured=True)
    featured_post = None
    if featured_posts:
        featured_post = featured_posts[0]
    subscriber_form = SubscriberForm()
    subscribe_succesfull = False
    if request.POST:
        subscriber_form = SubscriberForm(request.POST)
        if subscriber_form.is_valid():
            subscriber_form.save()
            subscribe_succesfull = True
            subscriber_form = SubscriberForm()
    context = {'posts':posts, 'top_posts':top_posts, 'recent_posts':recent_posts, 'subscriber_form':subscriber_form, 'subscribe_sucessfull':subscribe_succesfull, 'featured_post':featured_post}
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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    top_posts = BlogPost.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = BlogPost.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:3]
    tags = tag = Tag.objects.all()
    context = {'tag':tag, 'top_posts':top_posts, 'recent_posts':recent_posts, 'tags':tags }
    return render(request,'app/tag.html', context)