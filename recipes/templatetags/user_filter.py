from django import template
from django.contrib.auth import get_user_model
from ..models import FollowAuthor, FavoriteRecipes, Purchase

User = get_user_model()
register = template.Library()


@register.filter
def is_follow(user, author):
    return FollowAuthor.objects.filter(user=user, author=author).exists()


@register.filter
def is_favored_by(recipe, user):
    return FavoriteRecipes.objects.filter(favor=recipe, user=user).exists()


@register.filter
def is_in_shop_list_of(recipe, user):
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def remaining_recipes(number):
    last_digit = int(number) % 10
<<<<<<< HEAD
    if last_digit > 4 or last_digit == 0 or str(number).count('1') > 1:
=======
    if last_digit > 4 or last_digit == 0 or str(last_digit).count('1') > 1:
>>>>>>> ca1b883d613a22a93b0efee00a757763dd3d3007
        return f'{number} рецептов'
    elif last_digit > 1 and last_digit < 5:
        return f'{number} рецепта'
    elif last_digit == 1:
        return f'{number} рецепт'
