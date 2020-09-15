from . import models

from rest_framework import serializers

from django.contrib.auth import get_user_model


class BookListSerializer(serializers.ModelSerializer):
    """ Сериализатор списка книг """

    genre = serializers.SlugRelatedField(slug_field='name',
                                         queryset=models.Genre.objects.all(),
                                         many=True,
                                         required=True)

    language = serializers.SlugRelatedField(slug_field='name',
                                            queryset=models.Language.objects.all(),
                                            required=True)

    author = serializers.SlugRelatedField(slug_field='uuid',
                                          required=True,
                                          queryset=models.Author.objects.all())

    class Meta:
        model = models.Book
        exclude = ['id', ]
        read_only_fields = ['uuid', ]


class BookDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор объекта книги """

    language = serializers.SlugRelatedField(slug_field='name',
                                            queryset=models.Language.objects.all())

    genre = serializers.SlugRelatedField(slug_field='name',
                                         queryset=models.Genre.objects.all(),
                                         many=True)

    author = serializers.SlugRelatedField(slug_field='uuid',
                                          queryset=models.Author.objects.all())

    class Meta:
        model = models.Book
        exclude = ['id', ]
        read_only_fields = ['uuid', ]


class AuthorListSerializer(serializers.ModelSerializer):
    """ Сериализатор списка авторов """

    class Meta:
        model = models.Author
        exclude = ['id', ]
        read_only_fields = ['uuid']


class AuthorDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор объекта автора """

    class Meta:
        model = models.Author
        exclude = ['id', ]
        read_only_fields = ['uuid']


class FollowerSerializer(serializers.ModelSerializer):
    """ Сериализатор модели подписчика """

    class Meta:
        model = models.Follower
        exclude = ['id', ]
        read_only_fields = ['uuid', ]


class LanguageSerializer(serializers.ModelSerializer):
    """ Сериализатор модели языка """

    class Meta:
        model = models.Language
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор модели жанра """

    class Meta:
        model = models.Genre
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    """ Сериализатор списка объектов пользователей """

    full_name = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['uuid',
                  'full_name',
                  'username',
                  'password',
                  'email',
                  'date_joined', ]

        read_only_fields = ['uuid', 'last_login', 'is_active', 'is_superuser', 'is_staff', ]

    def create(self, validated_data: dict):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор объекта пользователя """

    class Meta:
        model = get_user_model()
        exclude = ['id', 'is_superuser', 'groups', 'user_permissions']
        read_only_fields = ['uuid', 'is_active', 'is_staff', 'last_login']

    def update(self, instance: models.User, validated_data: dict):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance