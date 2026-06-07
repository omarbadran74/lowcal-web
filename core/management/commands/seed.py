from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import User, FoodCategory, SubscriptionPlan


class Command(BaseCommand):
    help = 'Seed initial data'

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create(
                username='admin',
                password=make_password('admin123'),
                role=User.ROLE_ADMIN,
                first_name='',
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS('OK Admin user created: admin / admin123'))

        # Create cashier user
        if not User.objects.filter(username='cashier').exists():
            User.objects.create(
                username='cashier',
                password=make_password('cashier123'),
                role=User.ROLE_CASHIER,
                first_name='',
            )
            self.stdout.write(self.style.SUCCESS('OK Cashier user created: cashier / cashier123'))

        # Create subscription plans from the LowCal pricing table
        plans_data = [
            # Lose Weight (QAR prices from image)
            ('lose', 1, 7, 235), ('lose', 1, 14, 407), ('lose', 1, 21, 706), ('lose', 1, 28, 901),
            ('lose', 2, 7, 470), ('lose', 2, 14, 902), ('lose', 2, 21, 1352), ('lose', 2, 28, 1803),
            ('lose', 3, 7, 705), ('lose', 3, 14, 1352), ('lose', 3, 21, 1940), ('lose', 3, 28, 2537),
            ('lose', 4, 7, 907), ('lose', 4, 14, 1803), ('lose', 4, 21, 2587), ('lose', 4, 28, 3450),
            # Gain Weight
            ('gain', 1, 7, 286), ('gain', 1, 14, 538), ('gain', 1, 21, 806), ('gain', 1, 28, 1030),
            ('gain', 2, 7, 538), ('gain', 2, 14, 1013), ('gain', 2, 21, 1545), ('gain', 2, 28, 2061),
            ('gain', 3, 7, 806), ('gain', 3, 14, 1546), ('gain', 3, 21, 2217), ('gain', 3, 28, 2957),
            ('gain', 4, 7, 1030), ('gain', 4, 14, 2061), ('gain', 4, 21, 2957), ('gain', 4, 28, 3942),
        ]
        created = 0
        for goal, meals, days, price in plans_data:
            _, c = SubscriptionPlan.objects.get_or_create(
                goal=goal, meals_per_day=meals, days=days,
                defaults={'price': price}
            )
            if c:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'OK {created} subscription plans created'))

        # Create sample food categories
        categories_data = [
            ('بروتين الإفطار', 'breakfast'),
            ('كربوهيدرات الإفطار', 'breakfast'),
            ('سلطات وخضار', 'lunch'),
            ('بروتين الغداء', 'lunch'),
            ('بروتين العشاء', 'dinner'),
            ('سناكات صحية', 'snack'),
        ]
        for name, meal_type in categories_data:
            FoodCategory.objects.get_or_create(name=name, meal_type=meal_type)
        self.stdout.write(self.style.SUCCESS('OK Sample food categories created'))

        self.stdout.write(self.style.SUCCESS('\nSeed completed! Run the server with:'))
        self.stdout.write('   python manage.py runserver 8001')
