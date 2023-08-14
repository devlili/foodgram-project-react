from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import Favorite, Ingredient, Recipe, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
