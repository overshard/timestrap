from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken import views as authtokenviews

from . import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionViewSet)
router.register(r"clients", views.ClientViewSet)
router.register(r"projects", views.ProjectViewSet)
router.register(r"entries", views.EntryViewSet)
router.register(r"tasks", views.TaskViewSet)


urlpatterns = [
    path(r"api/auth/", include("rest_framework.urls")),
    path(r"api/auth_token/", authtokenviews.obtain_auth_token),
    path(r"api/", include(router.urls)),
]
