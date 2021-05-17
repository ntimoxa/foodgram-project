from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, FollowAuthor, FavoriteRecipes, Ingredient, RecipeIngredient
from django.core.paginator import Paginator
from .forms import RecipeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .resources import IngredientResource
from django.http import HttpResponse
from django.db.models import Sum

User = get_user_model()


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    favorites = []
    if request.user.is_authenticated:
        recipes_of_author = request.user.favorites.all()
        for favorite in recipes_of_author:
            favorites.append(favorite.favor)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'favorites': favorites,
    })


def single_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    author = recipe.author
    following = False
    favorite = False
    if request.user.is_authenticated:
        following = FollowAuthor.objects.filter(user=request.user, author=author).exists()
        favorite = FavoriteRecipes.objects.filter(user=request.user, favor=recipe).exists()
    return render(request, 'recipe_item.html', {
        'recipe': recipe,
        'following': following,
        'favorite': favorite,
    })


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        return redirect('index')
    return render(request, 'one_more_recipe.html', {'form': form})


def tags_index(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tags = Recipe.objects.filter(tag=tag)
    paginator = Paginator(tags, 6)
    active = 'active'
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if tag.id == 3:
        return render(request, 'index.html', {'page': page,
                                              'paginator': paginator,
                                              'active': active})
    elif tag.id == 2:
        return render(request, 'index.html', {'page': page,
                                              'paginator': paginator,
                                              'active2': active})
    else:
        return render(request, 'index.html', {'page': page,
                                              'paginator': paginator,
                                              'active3': active})


def tags_profile(request, username, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    author = get_object_or_404(User, username=username)
    tags = Recipe.objects.filter(tag=tag, author=author)
    paginator = Paginator(tags, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page,
                                            'paginator': paginator})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = False
    if request.user.is_authenticated:
        following = FollowAuthor.objects.filter(user=request.user, author=author).exists()
    recipes = Recipe.objects.filter(author=author)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page,
                                            'following': following,
                                            'paginator': paginator,
                                            'author': author})


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
    author = request.user
    favorites = Recipe.objects.filter(selected__user=author)
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite_index.html', {
        'page': page,
        'paginator': paginator,
        'favorites': favorites
    })


@login_required()
def shop_list(request):
    recipes = Recipe.objects.filter(purchase__user=request.user)
    return render(request, 'purchase_index.html', {
        'recipes': recipes,
    })


@login_required()
def download_ingredients_list(request):
    """Download list of ingredients for all recipes in shop list"""
    filename = "shop-list.txt"
    author = request.user
    recipes = RecipeIngredient.objects.filter(recipe__purchase__user=author)
    ingredients = IngredientResource()
    #recipes.order_by('ingredient__name').values(
    #    'ingredient__name',
     #   'ingredient__measure').annotate(
     #   total_count=Sum('amount'))
    result = ingredients.export(recipes)
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
