from rest_framework.views import APIView
from recipes.models import FavoriteRecipes, Ingredient, FollowAuthor, Purchase
from rest_framework import viewsets, mixins, filters
from .serializers import IngredientSerializer
from django.http import JsonResponse

SUCCESS_RESPONSE = JsonResponse({'success': True})
FAILED_RESPONSE = JsonResponse({'success': False}, status=400)


# Честно просидел всю ночь, делал через CreateModelMixin, Destroy..
# А также через роутеры и вьюсеты
# Но уткнулся в непонятное. Почему-то в сериализатор
# передавался параметр 'id' и ничего не создавалось
# Нагуглить не смог, наставники уже с нами не работают
# Сроки поджимают, поэтому решил оставить рабочий вариант

class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class AddToSubscriptions(APIView):
    """Add the person to User's subscriptions"""

    def post(self, request, format=None):
        create = FollowAuthor.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        if create:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE


class RemoveFromSubscriptions(APIView):
    """Remove the person from User's subscriptions"""

    def delete(self, request, pk, format=None):
        delete = FollowAuthor.objects.filter(
            user=request.user,
            author_id=pk
        ).delete()
        if delete:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE


class AddToFavorites(APIView):
    """Add the recipe to the favorites"""

    def post(self, request, format=None):
        create = FavoriteRecipes.objects.get_or_create(
            user=request.user,
            favor_id=request.data['id']
        )
        if create:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE


class RemoveFromFavorites(APIView):
    """Remove a Recipe from User's Favorites."""

    def delete(self, request, pk, format=None):
        delete = FavoriteRecipes.objects.filter(favor_id=pk,
                                                user=request.user).delete()
        if delete:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE


class AddToPurchases(APIView):
    """Add the recipe to shop list"""

    def post(self, request, format=None):
        create = Purchase.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        if create:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE


class RemoveFromPurchases(APIView):
    """Remove the recipe from shop list"""

    def delete(self, request, pk, format=None):
        delete = Purchase.objects.filter(
            user=request.user,
            recipe_id=pk,
        ).delete()
        if delete:
            return SUCCESS_RESPONSE
        return FAILED_RESPONSE
