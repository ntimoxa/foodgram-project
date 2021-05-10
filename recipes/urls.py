from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('recipe/<int:id>/', views.single_recipe, name="single_recipe"),
    path('recipe/new/', views.create_recipe, name='new'),
    path('recipe/tag/<int:tag_id>', views.tags_index, name='tag'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/<int:tag_id>', views.tags_profile, name='profile_tag'),
    path('follower/', views.follow_index, name='my_follow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
