import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


class Language(models.Model):
    """ Модель языка """
    name = models.CharField(verbose_name='Язык', max_length=200)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Модель жанра произведения """
    name = models.CharField(verbose_name='Жанр', max_length=100)

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return self.name


class Book(models.Model):
    """ Модель книги """
    uuid = models.UUIDField(verbose_name='Уникальный идентификатор книги', default=uuid.uuid4)
    author = models.ForeignKey('Author',
                               verbose_name='Автор книги',
                               null=True,
                               on_delete=models.SET_NULL)

    language = models.ForeignKey('Language',
                                 verbose_name='Язык на котором написана книга',
                                 max_length=200,
                                 on_delete=models.SET_NULL,
                                 null=True)

    genre = models.ManyToManyField(Genre, verbose_name='Жанры книги')

    title = models.CharField(verbose_name='Название книги', max_length=200)
    publication_year = models.DateTimeField(verbose_name='Год публикации')
    description = models.TextField(verbose_name='Описание книги', max_length=500, default='')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Author(models.Model):
    """ Модель автора """
    uuid = models.UUIDField(verbose_name='Уникальный идентификатор автора', default=uuid.uuid4, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    patronymic_name = models.CharField(verbose_name='Отчество', max_length=100)
    date_of_birth = models.DateTimeField(verbose_name='Дата рождения', null=True, blank=True)
    date_of_death = models.DateTimeField(verbose_name='Дата смерти', null=True, blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic_name}'


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователя """
    uuid = models.UUIDField(verbose_name='Уникальный идентификатор', default=uuid.uuid4, blank=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    email = models.EmailField(verbose_name='Адрес электронной почты', max_length=255, unique=True)
    full_name = models.CharField(verbose_name='Полное имя пользователя', max_length=128, blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    is_staff = models.BooleanField(verbose_name='Суперпользователь', default=False)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Follower(models.Model):
    """ Модель подписчика """
    uuid = models.UUIDField(verbose_name='Уникальный идентификатор подписчика', default=uuid.uuid4, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    patronymic_name = models.CharField(verbose_name='Отчество', max_length=100)
    email = models.EmailField(verbose_name='Электронный адрес')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return self.email