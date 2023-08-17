from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from users.serializers import CustumUserSerializer

from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    # tags = TagSerializer(many=True, read_only=True)
    author = CustumUserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(many=True)

    def create(self, validated_data):
        author = self.context.get("request").user
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            print(ingredient)
            # amount = ingredient.get("amount")
            # current_ingredient = get_object_or_404(
            #     Ingredient, id=ingredient.get("id")
            # )
            # RecipeIngredient.objects.create(
            #     ingredient=current_ingredient,
            #     recipe=recipe,
            #     amount=amount,
            # )

        return recipe

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        # read_only_fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = ShortRecipeSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ("recipe",)

    def to_representation(self, instance):
        recipe = instance.recipe
        return {
            "id": recipe.id,
            "name": recipe.name,
            "image": recipe.image,
            "cooking_time": recipe.cooking_time,
        }
