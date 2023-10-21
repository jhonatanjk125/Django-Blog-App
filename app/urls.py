from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('change_theme/', views.change_theme, name='change_theme'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.user_signup, name='signup'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_page, name='search_page'),
    path('bookmarks/<slug:slug>', views.bookmarks, name='bookmarks'),
    path('likes/<slug:slug>', views.likes, name='likes'),
    path('bookmarked_posts/', views.bookmarked_posts, name='bookmarked_posts'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('liked_posts/', views.liked_posts, name='liked_posts'),

]