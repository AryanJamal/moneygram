# Generated by Django 5.0.6 on 2024-07-26 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneygram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycards',
            name='amounts',
            field=models.DecimalField(decimal_places=4, max_digits=16),
        ),
    ]