from django.contrib import admin
from .models import Recipe, Ingredient, Tag, RecipeIngredient, FollowAuthor, FavoriteRecipes


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInLine,
    ]


class FollowAdmin(admin.ModelAdmin):
    model = FollowAuthor


admin.site.register(FavoriteRecipes)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(FollowAuthor, FollowAdmin)
# Register your models here.
