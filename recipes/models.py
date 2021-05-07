from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measure = models.CharField(max_length=126)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.name}, {self.measure}'


class Tag(models.Model):
    name = models.CharField(max_length=126)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    image = models.ImageField()
    description = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField()
    tag = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class FollowAuthor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_followgroup'),
        ]


class SelectedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selected')
    select = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class IngredientsPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase')
    purchase = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
