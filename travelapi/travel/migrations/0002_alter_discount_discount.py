# Generated by Django 5.0.4 on 2024-08-18 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
