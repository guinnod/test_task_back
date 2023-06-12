from django.urls import path
from . import views

urlpatterns = [
    path('posts', views.Posts.as_view()),
    path('register', views.Register.as_view()),
    path('login', views.Login.as_view()),
    path('user-data', views.UserData.as_view()),
    path('my-posts', views.MyPosts.as_view()),
    path('like', views.LikePost.as_view()),
]