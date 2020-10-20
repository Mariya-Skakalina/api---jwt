from django.urls import path
from .views import *

urlpatterns = [
    path('', SortedAndFilterPostViews.as_view()),
    path('register', RegisterUser.as_view()),
    path('auth', JSONWebTokenAuth.as_view()),
    path('post/<int:pk>', PostView.as_view()),
    path('add_post', AddPostView.as_view())
]