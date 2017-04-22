from django.conf.urls import url, include

from rest_framework import routers

from .views import UserViewSet, TimesheetViewSet, TaskViewSet, EntryViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'timesheets', TimesheetViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'entries', EntryViewSet)


urlpatterns = [
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/', include(router.urls)),
]
