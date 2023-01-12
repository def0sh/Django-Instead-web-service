from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('', ProjectHome.as_view(), name='projects'),
    path('project/<slug:slug>', FeedBackView.as_view(), name='project'),
    path('create', CreateProject.as_view(), name='create-project'),
    path('update-project/<str:pk>', UpdateProject.as_view(), name='update-project'),
    path('delete-project/<str:pk>', DeleteProject.as_view(), name='delete-project'),
    path('tag/<slug:tag_slug>', ProjectByTag.as_view(), name="tag"),

]