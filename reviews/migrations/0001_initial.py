# Generated by Django 2.2.5 on 2021-01-22 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0003_auto_20210122_1608'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('review', models.TextField()),
                ('accuracy', models.IntegerField(default=0)),
                ('communication', models.IntegerField(default=0)),
                ('cleanliness', models.IntegerField(default=0)),
                ('location', models.IntegerField(default=0)),
                ('check_in', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=0)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='rooms.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]