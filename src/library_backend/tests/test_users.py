from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class UserTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

    def test_get_list_users_for_admin(self):
        url = '/api/library/users/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        users = models.User.objects.all()
        serializer = serializers.UserListSerializer(instance=users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_users_for_user(self):
        url = '/api/library/users/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        users = models.User.objects.all()
        serializer = serializers.AuthorListSerializer(instance=users, many=True)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_instance_user_for_admin(self):
        url = f'/api/library/users/{self.user.uuid}/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        user = models.User.objects.get(uuid=self.user.uuid)
        serializer = serializers.UserDetailSerializer(instance=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_user_for_user(self):
        url = f'/api/library/users/{self.user.uuid}/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        user = models.User.objects.get(uuid=self.user .uuid)
        serializer = serializers.UserDetailSerializer(instance=user)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_for_admin(self):
        url = f'/api/library/users/'

        self.client.force_login(self.admin, None)

        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_pass+',
            'full_name': 'test test test'
        }

        serializer = serializers.UserListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.User.objects.count(), 3)

    def test_create_user_for_user(self):
        url = f'/api/library/users/'

        self.client.force_login(self.user, None)

        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_pass+',
            'full_name': 'test test test'
        }

        serializer = serializers.UserListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_for_admin(self):
        url = f'/api/library/users/{self.user.uuid}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_for_user(self):
        url = f'/api/library/users/{self.user.uuid}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_for_admin(self):
        url = f'/api/library/users/{self.user.uuid}/'

        self.client.force_login(self.admin, None)

        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_pass+',
            'full_name': 'test test test'
        }
        serializer = serializers.UserDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = models.User.objects.get(uuid=self.user.uuid)

        self.assertEqual(self.user.uuid, user.uuid)
        self.assertEqual(data.get('username'), user.username)
        self.assertEqual(data.get('email'), user.email)
        self.assertEqual(data.get('full_name'), user.full_name)

    def test_update_user_for_user(self):
        url = f'/api/library/users/{self.user.uuid}/'

        self.client.force_login(self.user, None)

        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_pass+',
            'full_name': 'test test test'
        }

        serializer = serializers.UserDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)







