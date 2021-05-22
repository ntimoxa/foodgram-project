import logging
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=Decimal(amount.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest
        logging.error(
            "Could not save form"
        )


def recipe_edit(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest
        logging.error(
            "Could not edit recipe"
        )