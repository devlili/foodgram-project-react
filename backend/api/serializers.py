from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Favorite, Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeFavoriteSerializer()

    class Meta:
        model = Favorite
        fields = ("recipe",)

    def to_representation(self, instance):
        recipe_data = instance.recipe
        return {
            "id": recipe_data.id,
            "name": recipe_data.name,
            "image": recipe_data.image.url,
            "cooking_time": recipe_data.cooking_time,
        }
