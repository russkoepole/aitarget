from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class GenreTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

        self.genre = models.Genre.objects.create(
            name='Роман'
        )

    def test_get_list_genres_for_admin(self):
        url = '/api/library/genres/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        genres = models.Genre.objects.all()
        serializer = serializers.GenreSerializer(instance=genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_genres_for_user(self):
        url = '/api/library/genres/'
        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_instance_genre_for_admin(self):
        url = f'/api/library/genres/{self.genre.id}/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        genre = models.Genre.objects.get(id=self.genre.id)
        serializer = serializers.GenreSerializer(instance=genre)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_genre_for_user(self):
        url = f'/api/library/genres/{self.genre.id}/'
        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        genre = models.Genre.objects.get(id=self.genre.id)
        serializer = serializers.LanguageSerializer(instance=genre)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_genre_for_admin(self):
        url = f'/api/library/genres/'

        self.client.force_login(self.admin, None)

        data = {
            'name': 'Повесть'
        }

        serializer = serializers.GenreSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Genre.objects.count(), 2)

    def test_create_language_for_user(self):
        url = f'/api/library/genres/'

        self.client.force_login(self.user, None)

        data = {
            'name': 'Повесть'
        }

        serializer = serializers.LanguageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_genre_for_admin(self):
        url = f'/api/library/genres/{self.genre.id}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_genre_for_user(self):
        url = f'/api/library/genres/{self.genre.id}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_language_for_admin(self):
        url = f'/api/library/genres/{self.genre.id}/'

        self.client.force_login(self.admin, None)

        data = {
            'name': 'Фантастика'
        }

        serializer = serializers.GenreSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        genre = models.Genre.objects.get(id=self.genre.id)

        self.assertEqual(self.genre.id, genre.id)
        self.assertEqual(data.get('name'), genre.name)

    def test_update_language_for_user(self):
        url = f'/api/library/genres/{self.genre.id}/'

        self.client.force_login(self.user, None)

        data = {
            'name': 'Фантастика'
        }

        serializer = serializers.GenreSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
