from django.urls import path, include
from . import views
from .api.views import (AddToFavorites, RemoveFromFavorites,
                        AddToSubscriptions, RemoveFromSubscriptions,
                        AddToPurchases, RemoveFromPurchases, IngredientViewSet)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

views_patterns = [
    path('', views.index, name="index"),
    path('recipe/<int:id>/', views.single_recipe, name="single_recipe"),
    path('recipe/new/', views.create_recipe, name='new'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit'),
    path('recipe/<int:id>/delete/', views.delete_recipe, name='recipe_delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('subscriptions/', views.follow_index, name='my_follow'),
    path('favorites/', views.favorites_index, name='favorites'),
    path('purchases/', views.shop_list, name='purchases'),
    path('export/', views.download_ingredients_list, name='get'),
]

api_patterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('subscriptions/', AddToSubscriptions.as_view()),
    path('subscriptions/<int:pk>/', RemoveFromSubscriptions.as_view()),
    path('purchases/', AddToPurchases.as_view()),
    path('purchases/<int:pk>/', RemoveFromPurchases.as_view()),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
