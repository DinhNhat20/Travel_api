# Generated by Django 5.0.4 on 2024-08-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_alter_discount_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='booking',
            name='full_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='booking',
            name='phone',
            field=models.CharField(default='', max_length=10),
        ),
    ]
