from rest_framework import status
from rest_framework.test import APITestCase

from src.library_backend import models
from src.library_backend import serializers


class FollowerTests(APITestCase):
    """ Юнит-тесты """

    def setUp(self) -> None:

        self.admin = models.User.objects.get(username='admin')
        self.user = models.User.objects.get(username='user')

        self.follower = models.Follower.objects.create(
            first_name='Иван',
            last_name='Иванов',
            patronymic_name='Иванович',
            email='ivanov@example.com'
        )

    def test_get_list_followers_for_admin(self):
        url = '/api/library/followers/'
        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        followers = models.Follower.objects.all()
        serializer = serializers.FollowerSerializer(instance=followers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_list_followers_for_user(self):
        url = '/api/library/followers/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        followers = models.Follower.objects.all()
        serializer = serializers.FollowerSerializer(instance=followers, many=True)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_instance_follower_for_admin(self):
        url = f'/api/library/followers/{self.follower.uuid}/'

        self.client.force_login(self.admin, None)

        response = self.client.get(path=url, format='json')

        follower = models.Follower.objects.get(uuid=self.follower.uuid)
        serializer = serializers.FollowerSerializer(instance=follower)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_instance_follower_for_user(self):
        url = f'/api/library/followers/{self.follower.uuid}/'

        self.client.force_login(self.user, None)

        response = self.client.get(path=url, format='json')

        follower = models.Follower.objects.get(uuid=self.follower.uuid)
        serializer = serializers.FollowerSerializer(instance=follower)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_follower_for_admin(self):
        url = f'/api/library/followers/'

        self.client.force_login(self.admin, None)

        data = {
            'first_name': 'Владислав',
            'last_name': 'Владиславов',
            'patronymic_name': 'Владиславович',
            'email': 'vladislavov@example.com'
        }

        serializer = serializers.FollowerSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Follower.objects.count(), 2)

    def test_create_follower_for_user(self):
        url = f'/api/library/followers/'

        self.client.force_login(self.user, None)

        data = {
            'first_name': 'Владислав',
            'last_name': 'Владиславов',
            'patronymic_name': 'Владиславович',
            'email': 'vladislavov@example.com'
        }

        serializer = serializers.FollowerSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_follower_for_admin(self):
        url = f'/api/library/followers/{self.follower.uuid}/'
        self.client.force_login(self.admin, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_follower_for_user(self):
        url = f'/api/library/followers/{self.follower.uuid}/'
        self.client.force_login(self.user, None)
        response = self.client.delete(path=url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_follower_for_admin(self):
        url = f'/api/library/followers/{self.follower.uuid}/'

        self.client.force_login(self.admin, None)

        data = {
            'first_name': 'Владислав',
            'last_name': 'Владиславов',
            'patronymic_name': 'Владиславович',
            'email': 'vladislavov@example.com'
        }
        serializer = serializers.FollowerSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        follower = models.Follower.objects.get(uuid=self.follower.uuid)

        self.assertEqual(self.follower.uuid, follower.uuid)
        self.assertEqual(data.get('first_name'), follower.first_name)
        self.assertEqual(data.get('last_name'), follower.last_name)
        self.assertEqual(data.get('email'), follower.email)
        self.assertEqual(data.get('patronymic_name'), follower.patronymic_name)

    def test_update_follower_for_user(self):
        url = f'/api/library/followers/{self.follower.uuid}/'

        self.client.force_login(self.user, None)

        data = {
            'first_name': 'Владислав',
            'last_name': 'Владиславов',
            'patronymic_name': 'Владиславович',
            'email': 'vladislavov@example.com'
        }
        serializer = serializers.FollowerSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)







