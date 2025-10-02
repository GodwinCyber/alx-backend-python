from rest_framework.routers import DefaultRouter
from .views import ConversationMessageView

router = DefaultRouter()
router.register(r"conversations/(?P<conversation_id>\d+)/messages", ConversationMessageView, basename="conversation-messages")

urlpatterns = router.urls
