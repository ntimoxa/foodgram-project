from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
from foodgram.settings import BASE_DIR
import os

CSV_FILE_PATH = os.path.join(BASE_DIR, 'fixtures/ingredients.csv')


class Command(BaseCommand):
    help = 'import data from csv to django_models'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding="utf8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, measure = row
                Ingredient.objects.get_or_create(name=name, measure=measure)
