from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, Ingredient
from django.core.paginator import Paginator
from .forms import RecipeForm


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def single_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_item.html', {'recipe': recipe})


def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        return redirect('index')
    return render(request, 'another_new.html', {'form': form})


def tags_index(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tags = Recipe.objects.filter(tag=tag)
    paginator = Paginator(tags, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})

class JustStaticPage(TemplateView):
    # В переменной template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница
    template_name = 'AuthIndex.html'
