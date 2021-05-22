from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField('Название тега', max_length=50, db_index=True)
    display_name = models.CharField('Название тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    measure = models.CharField(max_length=126,
                               verbose_name='Единица измерения')

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.name}, {self.measure}'


class Recipe(models.Model):
    title = models.CharField(max_length=256,
                             verbose_name='Название рецепта')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    image = models.ImageField(upload_to='posts/',
                              verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')

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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='amount')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = "Ингредиенты для рецепта"


class FollowAuthor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_followgroup'),
        ]


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites', blank=True, null=True)
    favor = models.ForeignKey(Recipe,
                              on_delete=models.CASCADE,
                              related_name='selected', blank=True, null=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favor'],
                name='unique_favorgroup'),
        ]

    def __str__(self):
        return f'{self.user.username}, {self.favor.title}'


class Purchase(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='purchase')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='purchase')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = "Покупки"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchasegroup'),
        ]

    def __str__(self):
        return f'{self.user} покупает {self.recipe}'
