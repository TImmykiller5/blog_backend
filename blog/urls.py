from django.urls import path
from . import views

urlpatterns = [
    path('', views.test.as_view(), name='test'),
    path('users/register',  views.registerUser.as_view(), name='register'),
    path('user/token',  views.MytokenObtainPairView.as_view(), name='get-user'),
    path('posts',  views.getPosts.as_view(), name='get-posts'),
    path('profile',  views.getOwnerPost.as_view(), name='get-owner-posts'),
    path('post/<str:pk>/',  views.getPost.as_view(), name='get-post'),
    path('create/post/',  views.createPost.as_view(), name='create-post'),
    path('create/post/<str:pk>/',  views.createPost.as_view(), name='edit-post'),
    path('delete/post/<str:pk>/',  views.deletePost.as_view(), name='delete-post'),
    path('comment/<str:pk>/',  views.commentHadler.as_view(), name='comment'),
]
