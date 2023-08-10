from djoser.views import UserViewSet

from .models import User
from .serializers import CustomUserCreateSerializer, CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return CustomUserCreateSerializer
        return CustomUserSerializer
