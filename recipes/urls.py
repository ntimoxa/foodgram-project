from django.urls import path
from . import views

urlpatterns = [
    path('', views.JustStaticPage.as_view(), name="index")
]
