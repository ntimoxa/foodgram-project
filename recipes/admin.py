from django.contrib import admin
from .models import (Recipe, Ingredient,
                     RecipeIngredient, FollowAuthor,
                     FavoriteRecipes, Purchase, Tag)


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measure']
    list_filter = ('name',)
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ('title',)
    search_fields = ('author', 'title',
                     'tag_breakfast', 'tag_lunch',
                     'tag_dinner')
    inlines = [
        IngredientInLine,
    ]


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'display_name')
    list_filter = ('title',)


class FollowAdmin(admin.ModelAdmin):
    class Meta:
        model = FollowAuthor


class FavoriteAdmin(admin.ModelAdmin):
    class Meta:
        model = FavoriteRecipes


admin.site.register(FavoriteRecipes, FavoriteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FollowAuthor, FollowAdmin)
admin.site.register(Purchase)
admin.site.register(Tag, TagAdmin)
