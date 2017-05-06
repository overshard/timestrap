from django.conf.urls import url, include

from rest_framework import routers

from .views import (UserViewSet, PermissionViewSet, ClientViewSet,
                    ProjectViewSet, EntryViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'entries', EntryViewSet)


urlpatterns = [
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),
]
