from django.contrib import admin
from django.urls import path, include

handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls')),
    path('about/', include('about.urls', namespace='about')),
    path('', include('recipes.urls')),
]
