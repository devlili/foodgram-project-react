from django.urls import include, path
from rest_framework import routers

app_name = "users"


# router.register(
#     "users/subscriptions", SubscriptionsViewSet, basename="subscriptions"
# )

urlpatterns = [
    path("", include("djoser.urls")),
]
