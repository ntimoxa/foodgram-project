from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("success")
    template_name = 'signup.html'


class SignUpDone(TemplateView):
    template_name = 'success_signup.html'
