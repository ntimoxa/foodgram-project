from django.contrib import admin
from .models import Recipe, Ingredient, Tag, RecipeIngredient


class IngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInLine,
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
# Register your models here.
