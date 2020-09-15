from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class AuthorTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

        self.author = models.Author.objects.create(
            first_name='Александр',
            last_name='Пушкин',
            patronymic_name='Сергеевич'
        )

    def test_get_list_authors_for_admin(self):
        url = '/api/library/authors/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        authors = models.Author.objects.all()
        serializer = serializers.AuthorListSerializer(instance=authors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_authors_for_user(self):
        url = '/api/library/authors/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        authors = models.Author.objects.all()
        serializer = serializers.AuthorListSerializer(instance=authors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_author_for_admin(self):
        url = f'/api/library/authors/{self.author.uuid}/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        author = models.Author.objects.get(uuid=self.author.uuid)
        serializer = serializers.AuthorDetailSerializer(instance=author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_author_for_user(self):
        url = f'/api/library/authors/{self.author.uuid}/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        author = models.Author.objects.get(uuid=self.author.uuid)
        serializer = serializers.AuthorDetailSerializer(instance=author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_author_for_admin(self):
        url = f'/api/library/authors/'

        self.client.force_login(self.admin, None)

        data = {
            'first_name': 'Владимир',
            'last_name': 'Маяковский',
            'patronymic_name': 'Владимирович'
        }

        serializer = serializers.AuthorListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Author.objects.count(), 2)

    def test_create_author_for_user(self):
        url = f'/api/library/authors/'

        self.client.force_login(self.user, None)

        data = {
            'first_name': 'Владимир',
            'last_name': 'Маяковский',
            'patronymic_name': 'Владимирович'
        }

        serializer = serializers.AuthorListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author_for_admin(self):
        url = f'/api/library/authors/{self.author.uuid}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author_for_user(self):
        url = f'/api/library/authors/{self.author.uuid}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author_for_admin(self):
        url = f'/api/library/authors/{self.author.uuid}/'

        self.client.force_login(self.admin, None)

        data = {
            'first_name': 'Сергей',
            'last_name': 'Есенин',
            'patronymic_name': 'Александрович'
        }

        serializer = serializers.AuthorDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        author = models.Author.objects.get(uuid=self.author.uuid)

        self.assertEqual(self.author.uuid, author.uuid)
        self.assertEqual(data.get('first_name'), author.first_name)
        self.assertEqual(data.get('last_name'), author.last_name)
        self.assertEqual(data.get('patronymic_name'), author.patronymic_name)

    def test_update_author_for_user(self):
        url = f'/api/library/authors/{self.author.uuid}/'

        self.client.force_login(self.user, None)

        data = {
            'first_name': 'Сергей',
            'last_name': 'Есенин',
            'patronymic_name': 'Александрович'
        }

        serializer = serializers.AuthorDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)







