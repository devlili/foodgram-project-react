from django.db import models

from users.models import User


class Tag(models.Model):
    """
    Модель для хранения информации о тегах.

    Поля:
    - name: название тега.
    - color: цветовой HEX-код. Например, "#49B64E".
    - slug: уникальное сокращение для URL.

    """

    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название тега"
    )
    color = models.CharField(max_length=7, verbose_name="Цветовой HEX-код")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для хранения информации об ингредиентах.

    Поля:
    - name: название ингредиента.
    - measurement_unit: единицы измерения.

    """

    name = models.CharField(
        max_length=255, verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=50, verbose_name="Единицы измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для хранения информации о рецептах.

    Поля:
    - author: автор публикации (связь с моделью User).
    - name: название рецепта.
    - image: изображение рецепта.
    - text: текстовое описание.
    - ingredients: ингредиенты блюда по рецепту (связь с моделью Ingredient/
      через промежуточную модель RecipeIngredient).
    - tags: теги рецепта (связь с моделью Tag).
    - cooking_time: время приготовления в минутах.

    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор публикации",
    )
    name = models.CharField(max_length=255, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="recipes/", verbose_name="Изображение рецепта"
    )
    text = models.TextField(verbose_name="Текстовое описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты блюда по рецепту",
    )
    tags = models.ManyToManyField(
        Tag, related_name="recipes", verbose_name="Теги"
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (минуты)"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """
    Модель для хранения информации об ингредиентах в рецептах.

    Поля:
    - recipe: рецепт (связь с моделью Recipe).
    - ingredient: ингредиент (связь с моделью Ingredient).
    - amount: количество ингредиента.

    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity} {self.unit}"
