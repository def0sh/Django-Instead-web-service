from django.urls import path, include, re_path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'projects', ProjectVieSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]