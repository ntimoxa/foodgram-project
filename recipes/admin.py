from django.contrib import admin
from .models import Recipe, Ingredient, Tag, RecipeIngredient, FollowAuthor, FavoriteRecipes, Purchase


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    inlines = [
        IngredientInLine,
    ]


class FollowAdmin(admin.ModelAdmin):
    model = FollowAuthor


class FavoriteAdmin(admin.ModelAdmin):
    model = FavoriteRecipes


admin.site.register(FavoriteRecipes, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(FollowAuthor, FollowAdmin)
admin.site.register(Purchase)
