from django.urls import path
from .views import SignUp, SignUpDone

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path('success/', SignUpDone.as_view(), name='success'),
]
