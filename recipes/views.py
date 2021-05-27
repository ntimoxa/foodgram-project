from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, FollowAuthor, Tag
from django.core.paginator import Paginator
from .forms import RecipeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from .tools import save_recipe, recipe_edit
from foodgram.settings import PAGINATION_PAGE_SIZE

User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


def index(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()

    recipes = Recipe.objects.filter(
        tags__title__in=tags
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()
    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'all_tags': all_tags
    })


def single_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_item.html', {
        'recipe': recipe,
    })


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        if recipe is not None:
            return redirect('single_recipe', id=recipe.id)
        return render(request, 'one_more_recipe.html', {
            'form': form,
            'valid': False})
    return render(request, 'one_more_recipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id=recipe_id)
    if not request.user.is_superuser:

        if request.user != recipe.author:
            return redirect('single_recipe', id=recipe_id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        recipe_edit(request, form, instance=recipe)
        return redirect(
            'single_recipe', id=recipe_id,
        )
    return render(
        request,
        'one_more_recipe.html',
        {
            'form': form,
            'recipe': recipe,
        }
    )


@login_required()
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile(request, username):
    """Show profile of user by it's username"""
    author = get_object_or_404(User, username=username)
    following = False
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    if request.user.is_authenticated:
        following = FollowAuthor.objects.filter(
            user=request.user,
            author=author).exists()
    recipes = author.recipes.filter(
        tags__title__in=tags
    ).prefetch_related('tags').distinct()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page,
                                            'following': following,
                                            'paginator': paginator,
                                            'author': author,
                                            'tags': tags,
                                            'all_tags': all_tags})


def page_not_found(request, exception):
    return render(request,
                  'misc/404.html',
                  {'path': request.path},
                  status=404
                  )


def server_error(request):
    return render(request,
                  'misc/500.html',
                  status=500)


@login_required()
def follow_index(request):
    """Show recipes of authors, following by user"""
    followers = User.objects.filter(following__user=request.user)
    paginator = Paginator(followers, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follower_index.html', {
        'page': page,
        'paginator': paginator,
    })


@login_required()
def favorites_index(request):
    """Show user's favorite recipes"""
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    favorites = Recipe.objects.filter(
        selected__user=request.user,
        tags__title__in=tags
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite_index.html', {
        'page': page,
        'paginator': paginator,
        'favorites': favorites,
        'tags': tags,
        'all_tags': all_tags
    })


@login_required()
def shop_list(request):
    """Show all the recipes from user's purchase list"""
    recipes = Recipe.objects.filter(purchase__user=request.user)
    return render(request, 'purchase_index.html', {
        'recipes': recipes,
    })


@login_required()
def download_ingredients_list(request):
    """Download list of ingredients for all recipes in shop list"""
    recipes = Recipe.objects.filter(purchase__user=request.user)
    ingredients = recipes.order_by('ingredients__name').values(
        'ingredients__name',
        'ingredients__measure').annotate(
        total_count=Sum('amount__amount'))
    content = ''
    for ingredient in ingredients:
        ingredient_str = (f'{ingredient["ingredients__name"]} - '
                          f'{ingredient["total_count"]} '
                          f'{ingredient["ingredients__measure"]}')
        content += f'{ingredient_str}' + '\n'
    filename = 'recipe_ingredients.txt'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
