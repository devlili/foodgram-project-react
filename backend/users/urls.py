from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register(
    "users/subscriptions", SubscriptionsViewSet, basename="subscriptions"
)

urlpatterns = [
    path("", include(router.urls)),
    # path("v1/auth/signup/", views.signup, name="token_get"),
    # path(
    #     "v1/auth/token/",
    #     views.get_token,
    #     name="token_send",
    # ),
]
