# Generated by Django 5.0.4 on 2024-08-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_booking_email_booking_full_name_booking_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
