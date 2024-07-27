# Generated by Django 5.0.6 on 2024-07-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneygram', '0002_alter_mycards_amounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycards',
            name='paidtwo',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='mycards',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
