from import_export import resources
from .models import RecipeIngredient


class IngredientResource(resources.ModelResource):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient__name', 'ingredient__measure', 'amount')
        export_order = ('ingredient__name', 'amount', 'ingredient__measure')
