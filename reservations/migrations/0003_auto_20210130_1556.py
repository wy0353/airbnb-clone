# Generated by Django 2.2.5 on 2021-01-30 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_bookedday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookedday',
            old_name='day',
            new_name='date',
        ),
    ]
