from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class LanguageTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

        self.language_rus = models.Language.objects.create(
            name='Русский'
        )

        self.language_en = models.Language.objects.create(
            name='Английский'
        )

    def test_get_list_languages_for_admin(self):
        url = '/api/library/languages/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        languages = models.Language.objects.all()
        serializer = serializers.LanguageSerializer(instance=languages, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_languages_for_user(self):
        url = '/api/library/languages/'
        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_instance_language_for_admin(self):
        url = f'/api/library/languages/{self.language_rus.id}/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        languages = models.Language.objects.get(id=self.language_rus.id)
        serializer = serializers.LanguageSerializer(instance=languages)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_language_for_user(self):
        url = f'/api/library/languages/{self.language_rus.id}/'
        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        languages = models.Language.objects.get(id=self.language_rus.id)
        serializer = serializers.LanguageSerializer(instance=languages)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_language_for_admin(self):
        url = f'/api/library/languages/'

        self.client.force_login(self.admin, None)

        data = {
            'name': 'Испанский'
        }

        serializer = serializers.LanguageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Language.objects.count(), 3)

    def test_create_language_for_user(self):
        url = f'/api/library/languages/'

        self.client.force_login(self.user, None)

        data = {
            'name': 'Испанский'
        }

        serializer = serializers.LanguageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_language_for_admin(self):
        url = f'/api/library/languages/{self.language_rus.id}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_language_for_user(self):
        url = f'/api/library/languages/{self.language_rus.id}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_language_for_admin(self):
        url = f'/api/library/languages/{self.language_rus.id}/'

        self.client.force_login(self.admin, None)

        data = {
            'name': 'Немецкий'
        }

        serializer = serializers.LanguageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        language = models.Language.objects.get(id=self.language_rus.id)

        self.assertEqual(self.language_rus.id, language.id)
        self.assertEqual(data.get('name'), language.name)

    def test_update_language_for_user(self):
        url = f'/api/library/languages/{self.language_rus.id}/'

        self.client.force_login(self.user, None)

        data = {
            'name': 'Немецкий'
        }

        serializer = serializers.LanguageSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
