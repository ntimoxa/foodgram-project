from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Tag, Ingredient, FollowAuthor, FavoriteRecipes
from django.core.paginator import Paginator
from .forms import RecipeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def single_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    author = recipe.author
    following = FollowAuthor.objects.filter(user=request.user, author=author).exists()
    return render(request, 'recipe_item.html', {
        'recipe': recipe,
        'following': following,
    })


@login_required
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


def tags_profile(request, username, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    author = get_object_or_404(User, username=username)
    tags = Recipe.objects.filter(tag=tag, author=author)
    paginator = Paginator(tags, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page})


@login_required
def follow(request, username):
    following = get_object_or_404(User, username=username)
    if not request.user == following:
        FollowAuthor.objects.get_or_create(user=request.user, author=following)
    return redirect('profile', username=username)


@login_required
def unfollow(request, username):
    following = get_object_or_404(User, username=username)
    FollowAuthor.objects.filter(user=request.user, author=following).delete()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = FollowAuthor.objects.filter(user=request.user, author=author).exists()
    recipes = Recipe.objects.filter(author=author)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page,
                                            'following': following,
                                            'author': author})


@login_required()
def follow_index(request):
    followers = User.objects.filter(following__user=request.user)
    paginator = Paginator(followers, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follower_index.html', {'page': page})


@login_required()
def favorites_index(request):
    author = request.user
    favorites = Recipe.objects.filter(selected__user=author)
    paginator = Paginator(favorites, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite_index.html', {'page': page})


@login_required()
def add_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    FavoriteRecipes.objects.get_or_create(user=user, favor=recipe)
    return redirect('favorites')


@login_required()
def delete_from_favorite(request, recipe_id):
    author = request.user
    favor = Recipe.objects.get(pk=recipe_id)
    FavoriteRecipes.objects.filter(user=author, favor=favor).delete()
    return redirect('favorites')
