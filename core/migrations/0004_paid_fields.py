from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_custom_days_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='المبلغ المدفوع'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='paid_by',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='طريقة الدفع'),
        ),
    ]
