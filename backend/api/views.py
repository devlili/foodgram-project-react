from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .permissions import IsOwnerOrAdmin
from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Favorite, Ingredient, Recipe, Tag


class CreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter


class FavoriteViewSet(CreateDeleteViewSet):  # APIView???
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get("recipes_id"))

    def get_queryset(self):
        return self.get_recipe().favorites.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, recipe=self.get_recipe())

    # def perform_destroy(self, instance):
    #     instance.delete()
