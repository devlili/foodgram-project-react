from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsOwnerOrAdmin
from .serializers import (
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeListSerializer,
    RecipeMinified,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для чтения списка ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для чтения списка тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для создания, чтения, обновления и удаления рецептов."""

    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ("update", "destroy"):
            return (IsOwnerOrAdmin(),)
        if self.action in ("create",):
            return (IsAuthenticated(),)
        return super().get_permissions()

    def add_to(self, model, user, pk):
        """Добавляет рецепт в указанную модель."""

        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {"Ошибка": "Рецепт уже был добавлен"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeMinified(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        """Удаляет рецепт из указанной модели."""

        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"Ошибка": "Рецепта нет или уже удален"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk):
        """Добавляет или удаляет рецепт из избранного у пользователя."""

        if request.method == "POST":
            return self.add_to(Favorite, request.user, pk)
        else:
            return self.delete_from(Favorite, request.user, pk)

    @action(detail=True, methods=["post", "delete"])
    def shopping_cart(self, request, pk):
        """Добавляет или удаляет рецепт из списка покупок пользователя."""

        if request.method == "POST":
            return self.add_to(ShoppingCart, request.user, pk)
        else:
            return self.delete_from(ShoppingCart, request.user, pk)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Создает файл со списком покупок пользователя для скачивания."""

        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__in_shopping_cart__user=user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .order_by("ingredient__name")
            .annotate(amount=Sum("amount"))
        )

        shopping_cart = f"Список покупок {user.get_full_name()}\n\n"
        for ingredient in ingredients:
            shopping_cart += (
                f'{ingredient["ingredient__name"].capitalize()},'
                f' {ingredient["amount"]}'
                f' {ingredient["ingredient__measurement_unit"]}\n'
            )
        shopping_cart += f"\n\nFoodgram {datetime.today():%d-%m-%Y}"

        filename = f"{user}_shopping_cart.txt"
        response = HttpResponse(shopping_cart, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response
