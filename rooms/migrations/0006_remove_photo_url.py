# Generated by Django 2.2.5 on 2021-01-24 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20210123_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='url',
        ),
    ]
