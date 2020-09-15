from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class BookTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

        self.language = models.Language.objects.create(
            name='Русский'
        )

        self.genre = models.Genre.objects.create(
            name='Роман'
        )

        self.author = models.Author.objects.create(
            first_name='Александр',
            last_name='Пушкин',
            patronymic_name='Сергеевич'
        )

        self.book = models.Book.objects.create(
            author=self.author,
            language=self.language,
            title='Капитанская дочка',
            publication_year=timezone.now(),
            description='Какое-то описание'
        )

        self.book.genre.add(self.genre)

    def test_get_list_books_for_admin(self):
        url = '/api/library/books/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        books = models.Book.objects.all()
        serializer = serializers.BookListSerializer(instance=books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_books_for_user(self):
        url = '/api/library/books/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        books = models.Book.objects.all()
        serializer = serializers.BookListSerializer(instance=books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_book_for_admin(self):
        url = f'/api/library/books/{self.book.uuid}/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        book = models.Book.objects.get(uuid=self.book.uuid)
        serializer = serializers.BookDetailSerializer(instance=book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_book_for_user(self):
        url = f'/api/library/books/{self.book.uuid}/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        book = models.Book.objects.get(uuid=self.book.uuid)
        serializer = serializers.BookDetailSerializer(instance=book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_for_admin(self):
        url = f'/api/library/books/'

        self.client.force_login(self.admin, None)

        data = {
            'author': self.author.uuid,
            'language': self.language.name,
            'genre': [self.genre.name, ],
            'title': 'Евгений Онегин',
            'publication_year': timezone.now()
        }

        serializer = serializers.BookListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Book.objects.count(), 2)

    def test_create_book_for_user(self):
        url = f'/api/library/books/'

        self.client.force_login(self.user, None)

        data = {
            'author': self.author.uuid,
            'language': self.language.name,
            'genre': [self.genre.name, ],
            'title': 'Евгений Онегин',
            'publication_year': timezone.now()
        }

        serializer = serializers.BookListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_for_admin(self):
        url = f'/api/library/books/{self.book.uuid}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_book_for_user(self):
        url = f'/api/library/books/{self.book.uuid}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_for_admin(self):
        url = f'/api/library/books/{self.book.uuid}/'

        self.client.force_login(self.admin, None)

        data = {
            'author': self.author.uuid,
            'language': self.language.name,
            'genre': [self.genre.name, ],
            'title': 'Евгений Онегин',
            'publication_year': timezone.now()
        }

        serializer = serializers.BookListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = models.Book.objects.get(uuid=self.book.uuid)

        self.assertEqual(data.get('author'), book.author.uuid)
        self.assertEqual(data.get('language'), book.language.name)
        self.assertEqual(data.get('genre')[0], book.genre.all()[0].name)
        self.assertEqual(data.get('title'), book.title)
        self.assertEqual(data.get('publication_year'), book.publication_year)

    def test_update_book_for_user(self):
        url = f'/api/library/books/{self.book.uuid}/'

        self.client.force_login(self.user, None)

        data = {
            'author': self.author.uuid,
            'language': self.language.name,
            'genre': [self.genre.name, ],
            'title': 'Евгений Онегин',
            'publication_year': timezone.now()
        }

        serializer = serializers.BookListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_special_book_for_admin(self):
        self.book.publication_year = timezone.now() + timezone.timedelta(days=10)
        self.book.save()

        url = '/api/library/books/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        books = models.Book.objects.all()
        serializer = serializers.BookListSerializer(instance=books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_special_book_for_user(self):
        self.book.publication_year = timezone.now() + timezone.timedelta(days=10)
        self.book.save()

        url = '/api/library/books/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, list())

    def test_search_books_for_admin(self):
        query_param = str(self.book.title)
        url = f'/api/library/books/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, data={'title': query_param})

        book = models.Book.objects.filter(title=query_param)
        serializer = serializers.BookListSerializer(instance=book, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_books_for_user(self):
        query_param = str(self.book.title)
        url = f'/api/library/books/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, data={'title': query_param})

        book = models.Book.objects.filter(title=query_param)
        serializer = serializers.BookListSerializer(instance=book, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)







