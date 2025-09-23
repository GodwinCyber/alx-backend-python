from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

