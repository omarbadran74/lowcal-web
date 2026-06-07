import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_CASHIER = 'cashier'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_CASHIER, 'Cashier'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CASHIER)

    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

    def is_cashier_role(self):
        return self.role == self.ROLE_CASHIER


class FoodCategory(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    name = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'فئة الطعام'
        verbose_name_plural = 'فئات الطعام'

    def __str__(self):
        return f"{self.name} ({self.get_meal_type_display()})"


class FoodItem(models.Model):
    categories = models.ManyToManyField(FoodCategory, related_name='items', verbose_name='الفئات')
    name = models.CharField(max_length=200, verbose_name='اسم الطبق')
    description = models.TextField(blank=True, verbose_name='الوصف')
    calories = models.PositiveIntegerField(null=True, blank=True, verbose_name='السعرات')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_meal_types(self):
        return list(self.categories.values_list('meal_type', flat=True).distinct())

    class Meta:
        verbose_name = 'طبق'
        verbose_name_plural = 'الأطباق'

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('gain', 'Gain Weight'),
    ]
    DAYS_CHOICES = [
        (7, '7 Days'),
        (14, '14 Days'),
        (21, '21 Days'),
        (28, '28 Days'),
    ]

    goal = models.CharField(max_length=10, choices=GOAL_CHOICES)
    meals_per_day = models.IntegerField()
    days = models.IntegerField(choices=DAYS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['goal', 'meals_per_day', 'days']

    def __str__(self):
        return f"{self.get_goal_display()} - {self.meals_per_day} meals - {self.days} days"


MEAL_TYPES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
]


class Subscriber(models.Model):
    name = models.CharField(max_length=200, verbose_name='الاسم')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, verbose_name='خطة الاشتراك')
    meal_types = models.CharField(max_length=100, verbose_name='أنواع الوجبات المشمولة')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    start_date = models.DateField(verbose_name='تاريخ البداية')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='أنشئ بواسطة')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مشترك'
        verbose_name_plural = 'المشتركون'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_meal_types_list(self):
        return [m.strip() for m in self.meal_types.split(',') if m.strip()]

    def get_meal_types_display_list(self):
        type_map = dict(MEAL_TYPES)
        return [type_map.get(m, m) for m in self.get_meal_types_list()]

    def total_days(self):
        return self.plan.days

    def get_subscriber_url(self):
        return f"/s/{self.token}/"


class DailyMealSelection(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='selections', verbose_name='المشترك')
    day_number = models.PositiveIntegerField(verbose_name='رقم اليوم')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES, verbose_name='نوع الوجبة')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الطبق المختار')

    class Meta:
        verbose_name = 'اختيار وجبة'
        verbose_name_plural = 'اختيارات الوجبات'
        unique_together = ['subscriber', 'day_number', 'meal_type']

    def __str__(self):
        return f"{self.subscriber.name} - اليوم {self.day_number} - {self.get_meal_type_display()}"


class DailySubmission(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='submissions', verbose_name='المشترك')
    day_number = models.PositiveIntegerField(verbose_name='رقم اليوم')
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='وقت الإرسال')

    class Meta:
        verbose_name = 'إرسال يومي'
        verbose_name_plural = 'الإرسالات اليومية'
        unique_together = ['subscriber', 'day_number']

    def __str__(self):
        return f"{self.subscriber.name} - اليوم {self.day_number}"
