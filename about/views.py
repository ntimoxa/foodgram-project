from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'info_pages/about_author.html'


class AboutTechView(TemplateView):
    template_name = 'info_pages/about_tech.html'


class AboutFoodView(TemplateView):
    template_name = 'info_pages/about_food.html'
