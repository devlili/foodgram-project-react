from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", CustomUserViewSet, basename="users")
# router.register(
#     "users/subscriptions", SubscriptionsViewSet, basename="subscriptions"
# )

urlpatterns = [
    path("", include(router.urls)),
]
