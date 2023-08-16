from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from drf_extra_fields.fields import Base64ImageField

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = "__all__"
        # read_only_fields = ('author',)


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeFavoriteSerializer()

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
