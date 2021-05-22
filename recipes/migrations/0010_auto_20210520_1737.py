# Generated by Django 3.2.2 on 2021-05-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210519_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriterecipes',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='followauthor',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'Покупка', 'verbose_name_plural': 'Покупки'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецепта'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag_breakfast',
            field=models.BooleanField(default=False, verbose_name='Завтрак'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag_dinner',
            field=models.BooleanField(default=False, verbose_name='Ужин'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag_lunch',
            field=models.BooleanField(default=False, verbose_name='Обед'),
        ),
    ]