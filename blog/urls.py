from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='blog_home'),
    path('posts/', views.PostListView.as_view(), name='posts_list'),
    path('posts/<pk>/', views.post_details, name='post_details'),
    path('posts/<pk>/comment/', views.post_comment, name='post_comment'),
    path('ticket', views.ticket, name='ticket'),
    path('new-post', views.new_post, name='new_post'),
    path('users/<id>', views.show_user, name='show_user'),
    path('search', views.post_search, name='post_search')
]
