from django.contrib import admin
from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('home' , views.HomeView.as_view() , name='home'),
    path('post/<int:id>/<slug:slug>' , views.PostDetailView.as_view() , name='post-detail'),
    path('post/delete/<int:post_id>' , views.PostDeleteView.as_view() , name='post-delete'),
    path('post/update/<int:post_id>' , views.PostUpdateView.as_view() , name='post-update'),
    path('post/create' , views.PostCreateView.as_view() , name='post-create'),
    path('reply/<int:post_id>/<int:comment_id>' , views.ReplyView.as_view() ,name='reply'),
    path('like/<int:post_id>' , views.LikeView.as_view() , name='like')
]
