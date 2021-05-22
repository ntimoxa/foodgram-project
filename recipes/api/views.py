from rest_framework.views import APIView
from recipes.models import FavoriteRecipes, Ingredient, FollowAuthor, Purchase
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins, filters
from .serializers import IngredientSerializer


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name',)


class AddToSubscriptions(APIView):
    """Add the person to User's subscriptions"""

    def post(self, request, format=None):
        FollowAuthor.objects.get_or_create(
            user=request.user,
            author_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromSubscriptions(APIView):
    """Remove the person from User's subscriptions"""

    def delete(self, request, pk, format=None):
        FollowAuthor.objects.filter(
            user=request.user,
            author_id=pk
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToFavorites(APIView):
    """Add the recipe to the favorites"""

    def post(self, request, format=None):
        FavoriteRecipes.objects.get_or_create(
            user=request.user,
            favor_id=request.data['id']
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorites(APIView):
    """Remove a Recipe from User's Favorites."""

    def delete(self, request, pk, format=None):
        FavoriteRecipes.objects.filter(favor_id=pk,
                                       user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToPurchases(APIView):
    """Add the recipe to shop list"""

    def post(self, request, format=None):
        Purchase.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromPurchases(APIView):
    """Remove the recipe from shop list"""

    def delete(self, request, pk, format=None):
        Purchase.objects.filter(
            user=request.user,
            recipe_id=pk,
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
