from rest_framework import routers

from src.apps.topics import views

app_name = "topics"


router = routers.DefaultRouter(trailing_slash=False)

router.register(r"", views.TopicViewSet, basename="topics")
router.register(r"messages/", views.MessageViewSet, basename="messages")
router.register(r"subs/", views.SubViewSet, basename="subs")

urlpatterns = router.urls
