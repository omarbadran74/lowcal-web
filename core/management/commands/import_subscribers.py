"""
Management command to import/update subscribers from Excel data.
Usage: python manage.py import_subscribers
"""
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from core.models import Subscriber, SubscriptionPlan

SUBSCRIBERS = [
    # (name, phone, start_date, goal, meals_per_day, days, meal_types, paid_amount, paid_by, notes)
    ('Abdullah Talel Al Sliti', '77646646',  '2026-05-28', 'lose', 4, 28, 'breakfast,lunch,dinner,snack', 2030, 'Bank', ''),
    ('AL Dana',                 '66060074',  '2026-05-03', 'lose', 2, 63, 'lunch,snack',                  2460, 'Bank', ''),
    ('Kholud (Branch Al Wakrah)', '33381311','2026-05-30', 'lose', 2, 28, 'lunch,dinner',                 1803, 'Bank', ''),
    ('Elqeed',                  '70611119',  '2026-05-12', 'gain', 2, 28, 'lunch,dinner',                 1854, 'Bank', 'Requested salad'),
    ('Mohammed Salem Al-Marri', '70999936',  '2026-06-07', 'gain', 4, 28, 'breakfast,lunch,dinner,snack', 2200, 'Bank', ''),
    ('Muhammad Rashid',         '66333327',  '2026-05-19', 'lose', 3, 28, 'lunch,dinner,snack',           1800, 'Bank', ''),
    ("Naif Al Atibi's Wife",    '',          '2026-05-27', 'lose', 3, 28, 'lunch,dinner,snack',           None, '',     ''),
]

# Existing subscribers to update payment info (phone → paid_amount, paid_by)
UPDATE_PAYMENT = [
    ('55093000', 810,  'Card'),
    ('33152002', 1803, 'Bank'),
    ('77734526', 896,  'by rejeem'),
    ('33955597', 2363, 'Bank'),
    ('51363666', 1668, 'Bank'),
]


class Command(BaseCommand):
    help = 'Import subscribers from Excel data and update payment info'

    def handle(self, *args, **options):
        # Step 1: Update payment info on existing subscribers
        self.stdout.write('--- Updating existing payment info ---')
        for phone, amount, paid_by in UPDATE_PAYMENT:
            try:
                sub = Subscriber.objects.get(phone=phone)
                sub.paid_amount = amount
                sub.paid_by = paid_by
                sub.save(update_fields=['paid_amount', 'paid_by'])
                self.stdout.write(self.style.SUCCESS(f'  Updated: {sub.name} → QAR {amount} ({paid_by})'))
            except Subscriber.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Not found: phone {phone}'))

        # Step 2: Add missing subscribers
        self.stdout.write('\n--- Adding new subscribers ---')
        for name, phone, start_date_str, goal, meals_per_day, days, meal_types, paid_amount, paid_by, notes in SUBSCRIBERS:
            # Skip if already exists (match by name or phone)
            if phone and Subscriber.objects.filter(phone=phone).exists():
                self.stdout.write(f'  Skipped (exists): {name}')
                continue
            if not phone and Subscriber.objects.filter(name__iexact=name).exists():
                self.stdout.write(f'  Skipped (exists): {name}')
                continue

            # Find best matching plan
            plan = (
                SubscriptionPlan.objects.filter(goal=goal, meals_per_day=meals_per_day, days=days).first()
                or SubscriptionPlan.objects.filter(goal=goal, meals_per_day=meals_per_day).first()
                or SubscriptionPlan.objects.filter(goal=goal).first()
            )
            if not plan:
                self.stdout.write(self.style.ERROR(f'  No plan found for {name} (goal={goal}, meals={meals_per_day}) — skipped'))
                continue

            custom_days = days if days != plan.days else None
            start = parse_date(start_date_str)

            sub = Subscriber.objects.create(
                name=name,
                phone=phone or '',
                plan=plan,
                meal_types=meal_types,
                start_date=start,
                custom_days=custom_days,
                paid_amount=paid_amount,
                paid_by=paid_by,
                notes=notes,
            )
            self.stdout.write(self.style.SUCCESS(
                f'  Created: {name} | plan: {plan} | days: {sub.total_days()} | QAR {paid_amount or "-"}'
            ))

        self.stdout.write('\nDone.')
