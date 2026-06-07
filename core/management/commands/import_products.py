import csv
import os
from django.core.management.base import BaseCommand
from core.models import FoodCategory, FoodItem

CATEGORY_MAP = {
    'cat-01': ('إفطار',             'breakfast'),
    'cat-02': ('شوربات',            'lunch'),
    'cat-03': ('سلطات',             'lunch'),
    'cat-04': ('برجر لحم بقري',     'lunch'),
    'cat-05': ('برجر دجاج',         'lunch'),
    'cat-06': ('سندويشات',          'lunch'),
    'cat-07': ('لحم بقري وستيك',    'dinner'),
    'cat-08': ('أطباق الدجاج',      'dinner'),
    'cat-09': ('سوشي ومأكولات بحرية','dinner'),
    'cat-10': ('أسماك',             'dinner'),
    'cat-11': ('أسماك',             'dinner'),  # same as cat-10
    'cat-12': ('مرفقات',            'lunch'),
    'cat-13': ('مشروبات',           'snack'),
    'cat-14': ('برياني وأرز عربي',  'lunch'),
    'cat-15': ('بيتزا',             'lunch'),
    'cat-16': ('أطباق دولية',       'dinner'),
    'cat-17': ('باستا',             'dinner'),
    'cat-18': ('حلويات',            'snack'),
    'cat-19': ('أكاي',              'snack'),
    'cat-20': ('عصائر وسموذي',      'snack'),
    'cat-21': ('إضافات',            'snack'),
    'pb-001': ('منتجات بروتين',     'snack'),
}

SKIP_NAMES = {'Body Building', 'Weight loss', 'Subscription'}


class Command(BaseCommand):
    help = 'Import products from Foodics CSV export'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the products CSV file')
        parser.add_argument('--clear', action='store_true', help='Clear existing items before import')

    def handle(self, *args, **options):
        csv_path = options['csv_file']
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_path}'))
            return

        if options['clear']:
            FoodItem.objects.all().delete()
            FoodCategory.objects.all().delete()
            self.stdout.write('Cleared existing data')

        # Build category objects (unique by name+meal_type)
        cat_objects = {}
        for ref, (name, meal_type) in CATEGORY_MAP.items():
            key = (name, meal_type)
            if key not in cat_objects:
                cat, _ = FoodCategory.objects.get_or_create(name=name, meal_type=meal_type, defaults={'is_active': True})
                cat_objects[key] = cat
            # map ref -> category object
            CATEGORY_MAP[ref] = cat_objects[(name, meal_type)]

        self.stdout.write(f'Categories ready: {len(cat_objects)}')

        imported = skipped = 0

        with open(csv_path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name_en = row.get('name', '').strip()
                name_ar = row.get('name_localized', '').strip()
                is_active = row.get('is_active', 'Yes') == 'Yes'
                cat_ref = row.get('category_reference', '').strip()

                if name_en in SKIP_NAMES or not is_active or not cat_ref or cat_ref not in CATEGORY_MAP:
                    skipped += 1
                    continue

                display_name = name_en  # always use English name
                description = row.get('description', '').strip()

                calories = None
                raw_cal = row.get('calories', '').strip()
                if raw_cal:
                    try:
                        calories = int(float(raw_cal))
                    except ValueError:
                        pass

                item, created = FoodItem.objects.get_or_create(
                    name=display_name,
                    defaults={'description': description, 'calories': calories, 'is_active': True}
                )
                if not created:
                    if description:
                        item.description = description
                    if calories:
                        item.calories = calories
                    item.save()

                cat_obj = CATEGORY_MAP[cat_ref]
                item.categories.add(cat_obj)
                imported += 1

        self.stdout.write(self.style.SUCCESS(f'Done — imported: {imported}, skipped: {skipped}'))
