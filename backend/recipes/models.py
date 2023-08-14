from django.core.validators import MinValueValidator
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
        max_length=200,
        db_index=True,
        verbose_name="Название тега",
    )
    color = models.CharField(max_length=7, verbose_name="Цветовой HEX-код")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Уникальный слаг",
    )

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
        max_length=200,
        db_index=True,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения",
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
    - ingredients: список ингредиентов (связь с моделью Ingredient/
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
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Название рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/", verbose_name="Изображение рецепта"
    )
    text = models.TextField("Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Список ингредиентов",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveIntegerField(
        "Время приготовления (в минутах)"
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
    amount = models.PositiveIntegerField(
        "Количество",
        validators=[MinValueValidator(1, message="Минимальное количество 1!")],
    )

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity} {self.unit}"


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite_recipe"
            )
        ]

    def __str__(self):
        return f"Рецепт {self.recipe.name} в избранном у {self.user.username}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart_recipe"
            ),
        )

    def __str__(self):
        return (
            f"Рецепт {self.recipe.name} в списке покупок у"
            f" {self.user.username}"
        )
