from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import CustomUserSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = "__all__"


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов рецепта."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class CreateRecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов создания рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ("id", "amount")


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления рецепта."""

    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateRecipeIngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        exclude = ("pub_date",)

    def validate_tags(self, value):
        if not value:
            raise ValidationError("Добавьте как минимум 1 тег.")
        return value

    def validate_ingredients(self, value):
        if not value:
            raise ValidationError("Добавьте как минимум 1 ингредиент.")

        ingredients = [item["id"] for item in value]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                "Ингридиенты не должны повторяться!"
            )

        return value

    def add_ingredients(self, ingredients, recipe):
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient.get("id"),
                    amount=ingredient.get("amount"),
                )
                for ingredient in ingredients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get("request").user
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        self.add_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            instance.ingredients.clear()
            self.add_ingredients(ingredients, instance)
        if "tags" in validated_data:
            instance.tags.set(validated_data.pop("tags"))
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов."""

    author = CustomUserSerializer(read_only=True)
    image = serializers.ReadOnlyField(source="image.url")
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsSerializer(
        many=True, required=True, source="recipe_ingredients"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeMinified(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка рецептов."""

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")
