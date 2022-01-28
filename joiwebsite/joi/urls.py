from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

from django.urls import include, path
from rest_framework import routers
import rest_framework.authtoken.views as authtokenviews

ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', views.UserViewSet)
ROUTER.register(r'groups', views.GroupViewSet)
ROUTER.register(r'residents', views.ResidentViewSet)
ROUTER.register(r'memoryboxtypes', views.MemoryBoxTypeViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('spotify', views.spotify, name='spotify'),
    re_path(r'^(?P<version>v1)/', include(ROUTER.urls)),  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# login url for browsable api
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
]