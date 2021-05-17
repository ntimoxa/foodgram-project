from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measure = models.CharField(max_length=126, verbose_name='Единица измерения')

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
    title = models.CharField(max_length=256, verbose_name='Название рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор')
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    tag = models.ManyToManyField(Tag, related_name='recipes', verbose_name='Теги')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = "Рецепты"
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='amount')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='amount')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')


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


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', blank=True, null=True)
    favor = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='selected', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favor'],
                name='unique_favorgroup'),
        ]

    def __str__(self):
        return f'{self.user.username}, {self.favor.title}'


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='purchase')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchasegroup'),
        ]

    def __str__(self):
        return f'{self.user} покупает {self.recipe}'
