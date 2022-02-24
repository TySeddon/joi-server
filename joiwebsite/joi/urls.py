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
ROUTER.register(r'carepartnerresidents', views.CarePartnerResidentViewSet)
ROUTER.register(r'devices', views.DeviceViewSet)
ROUTER.register(r'memoryboxtypes', views.MemoryBoxTypeViewSet)
ROUTER.register(r'memoryboxtypes', views.MemoryBoxTypeViewSet)
ROUTER.register(r'memoryboxes', views.MemoryBoxViewSet)
ROUTER.register(r'memoryboxsessions', views.MemoryBoxSessionViewSet)
ROUTER.register(r'memoryboxsessionmedia', views.MemoryBoxSessionMediaViewSet)
ROUTER.register(r'mediainteractions', views.MediaInteractionViewSet)
ROUTER.register(r'slideshows', views.SlideshowViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('joi_home', views.joi_home, name='joi_home'),
    path('spotify', views.spotify, name='spotify'),
    path('slideshow', views.slideshow, name='slideshow'),
    path('reports/memorybox_sessions', views.memorybox_sessions_list, name='memorybox_sessions_list'),
    path('reports/memorybox_session', views.memorybox_session_report, name='memorybox_session_report'),
    re_path(r'^(?P<version>v1)/users/login/$', authtokenviews.obtain_auth_token),
    re_path(r'^(?P<version>v1)/', include(ROUTER.urls)),  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# login url for browsable api
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
]