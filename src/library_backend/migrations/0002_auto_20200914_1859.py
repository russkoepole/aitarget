import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_initial_data(apps, schema_editor):

    User = apps.get_model('library_backend', 'User')

    # Создаю суперпользователя
    User.objects.get_or_create(
        email='admin@example.com',
        username='admin',
        password=make_password('admin00+'),
        full_name='Администратор',
        is_superuser=True,
        is_active=True,
        is_staff=True
    )

    # Ну и пользователя обычного еще
    User.objects.get_or_create(
        email='user@example.com',
        username='user',
        password=make_password('user000+'),
        full_name='Пользователь',
        is_superuser=False,
        is_active=True,
        is_staff=False
    )


def delete_initial_data(apps, schema_editor):

    User = apps.get_model('library_backend', 'User')

    try:
        User.objects.get(username='admin').delete()
        User.objects.get(username='user').delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('library_backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, delete_initial_data)
    ]
