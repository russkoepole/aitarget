from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models, serializers
from .utils import permissions

from django.utils import timezone

from .utils.services import email_client

""" 

    Классы видов для получения списков объектов и их создание

"""


class BookListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка всех книг и создания новой"""
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookListSerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        title = self.request.query_params.get('title', None)

        # Фильтрация по названию книги
        if title:
            self.queryset = self.queryset.all().filter(title=title)

        # Если юзер является админом - вернем все книги
        if user.is_staff:
            self.queryset = self.queryset.all()
        # Иначе вернем только те, которые доступны до сегодняшнего дня
        else:
            self.queryset = self.queryset.all().filter(publication_year__lte=timezone.now())

        return self.queryset

    def perform_create(self, serializer):
        serializer.save()

        email_client(book_title=serializer.validated_data.get('title'))


class AuthorListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка всех авторов и создания нового"""
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorListSerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly, IsAuthenticated]


class FollowerListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка подписчиков и создания нового """
    queryset = models.Follower.objects.all()
    serializer_class = serializers.FollowerSerializer


class LanguageListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка доступных языков и создания нового """
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class UserListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка пользователей и создания нового """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserListSerializer


class GenreListView(generics.ListCreateAPIView):
    """ Класс вида для получения списка жанров и создания нового """
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


"""
 
    Классы видов для получения объектов моделей, их изменение и удаление

"""


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта книги, его изменение и удаление """
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookDetailSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAdminUserOrReadOnly, IsAuthenticated]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта автора, его изменение и удаление """
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorDetailSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAdminUserOrReadOnly, IsAuthenticated]


class FollowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта подписчика, его изменение и удаление """
    queryset = models.Follower.objects.all()
    serializer_class = serializers.FollowerSerializer
    lookup_field = 'uuid'


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта пользователя, его изменение и удаление"""
    queryset = models.User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    lookup_field = 'uuid'


class LanguageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта языка, его изменение и удаление"""
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    lookup_field = 'id'


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Класс вида для получения объекта жанра, его изменение и удаление"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'id'
