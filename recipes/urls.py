from django.urls import path, include
from . import views
from .api.views import AddToFavorites, RemoveFromFavorites, AddToSubscriptions, RemoveFromSubscriptions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

views_patterns = [
    path('', views.index, name="index"),
    path('recipe/<int:id>/', views.single_recipe, name="single_recipe"),
    path('recipe/new/', views.create_recipe, name='new'),
    path('recipe/tag/<int:tag_id>', views.tags_index, name='tag'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/<int:tag_id>', views.tags_profile, name='profile_tag'),
    path('subscriptions/', views.follow_index, name='my_follow'),
    path('favorites/', views.favorites_index, name='favorites'),
]

api_patterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:pk>/', RemoveFromFavorites.as_view()),
    path('subscriptions/', AddToSubscriptions.as_view()),
    path('subscriptions/<int:pk>/', RemoveFromSubscriptions.as_view()),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
