from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm, NewUserForm, SubscriberForm
from .models import BlogPost, Comment, Tag, Author, WebsiteMeta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
def home(request):
    """Handles any request to go to the main page, this includes fetching the top posts, recents posts and the featured post."""
    posts = BlogPost.objects.all()
    top_posts = BlogPost.objects.all().order_by('-view_count')[0:3]
    recent_posts = BlogPost.objects.all().order_by('-last_updated')[0:3]
    featured_posts = BlogPost.objects.filter(is_featured=True)
    featured_post = None
    website_info = None
    if featured_posts:
        featured_post = featured_posts[0]
    subscriber_form = SubscriberForm()
    subscribe_succesfull = False
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    if request.POST:
        subscriber_form = SubscriberForm(request.POST)
        if subscriber_form.is_valid():
            subscriber_form.save()
            request.session['subscribed']=True
            subscribe_succesfull = True
            subscriber_form = SubscriberForm()
    context = {'posts':posts, 'top_posts':top_posts, 'recent_posts':recent_posts, 'subscriber_form':subscriber_form, 'subscribe_sucessfull':subscribe_succesfull, 'featured_post':featured_post, 'website_info':website_info}
    return render(request, 'app/index.html', context)


def about(request):
    """Handles the request to go to the about page, this view will get the about information from the website meta."""
    website_info = None
    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {'website_info':website_info}
    return render(request, 'app/about.html', context)
    


def post_page(request, slug):
    """Handles any request to go to a specific post, it fetches the post itself, comments, replies,
    top authors, recent posts and related posts. It also handles the logic for posting comments
    and replies."""
    post = BlogPost.objects.get(post_slug = slug)
    comments = Comment.objects.filter(post=post, parent=None)
    form = CommentForm()
    number_of_likes = post.likes.count()
    number_of_comments = comments.count()
    for comment in comments:
        number_of_replies = comment.replies.count()
        number_of_comments += number_of_replies
    #Check if post is bookmarked by user
    is_bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        is_bookmarked=True
    
    #Check if post is liked by user
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    
    #Update number of views
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()
    
    #Content for sidebar
    recent_posts = BlogPost.objects.exclude(post_slug = slug).order_by('-last_updated')
    top_authors = User.objects.annotate(number=Count('blogpost')).order_by('-number')
    tags = Tag.objects.all()
    related_posts = BlogPost.objects.exclude(post_slug = slug).filter(author=post.author)

    context = {'post':post, 'form':form, 'comments':comments, 'is_bookmarked':is_bookmarked, 
               'is_liked':is_liked, 'number_of_likes':number_of_likes, 'recent_posts':recent_posts,
               'top_authors':top_authors, 'tags':tags, 'related_posts':related_posts, 'number_of_comments':number_of_comments
               }

    #Comments logic
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
    """Handles the request to go to a tag page where it'll fetch all
    the specific posts for a particular tag."""
    tag = Tag.objects.get(slug=slug)
    top_posts = BlogPost.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = BlogPost.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:3]
    tags = Tag.objects.all()
    context = {'tag':tag, 'top_posts':top_posts, 'recent_posts':recent_posts, 'tags':tags }
    return render(request,'app/tag.html', context)

def author_page(request, slug):
    """Handles the request to go to the author page where it'll fetch
    all the posts made by that particular author."""
    author = Author.objects.get(slug=slug)
    top_posts = BlogPost.objects.filter(author=author.user).order_by('-view_count')[0:2]
    recent_posts = BlogPost.objects.filter(author=author.user).order_by('-last_updated')[0:3]
    authors = User.objects.annotate(number=Count('blogpost')).order_by('-number')
    context = {'author':author, 'top_posts':top_posts, 'recent_posts':recent_posts, 'authors':authors }
    return render(request,'app/author.html', context)

def search_page(request):
    """Handles the request to go to the search page and returns the query information
    based on the user's search."""
    search_query = ''
    if request.GET.get('q'):
        search_query=request.GET.get('q')
    posts = BlogPost.objects.filter(title__icontains=search_query)
    print('Search:', search_query)
    context = {'posts':posts, 'search_query':search_query}
    return render(request,'app/search.html', context)

def user_signup(request):
    """Handles the signup request, saves any new sign up to the database."""
    form = NewUserForm()
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    context = {'form':form}
    return render(request,'registration/register.html', context)

def bookmarks(request,slug):
    """Handles the request to bookmark/remove bookmark for a post (only for logged in users)."""
    post = get_object_or_404(BlogPost, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def likes(request,slug):
    """Handles the request to like/dislike a post (only for logged in users)."""
    post = get_object_or_404(BlogPost, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def bookmarked_posts(request):
    """Handles the request to the bookmarked page (only for logged in users)."""
    bookmarked_posts = BlogPost.objects.filter(bookmarks=request.user)
    context = {'bookmarked_posts':bookmarked_posts}
    return render(request,'app/bookmarked_posts.html', context)

def all_posts(request):
    """Fetches all posts (for both visitors and logged in users)."""
    all_posts = BlogPost.objects.all()
    context = {'all_posts':all_posts}
    return render(request,'app/all_posts.html', context)

def liked_posts(request):
    """Handles the request to the liked page (only for logged in users)."""
    liked_posts = BlogPost.objects.filter(likes=request.user)
    context = {'liked_posts':liked_posts}
    return render(request,'app/liked_posts.html', context)

def change_theme(request):
    """Handles the request to toggle between dark mode and light mode"""
    if 'dark_mode' in request.session:
        request.session['dark_mode'] = not request.session.get('dark_mode')
    else:
        request.session['dark_mode'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))