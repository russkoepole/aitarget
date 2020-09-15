from django.core.mail import send_mail
from django.conf import settings

from src.library_backend import models


def email_client(book_title: str) -> None:
    """
    Функция отправляет письма на почту подпичикам библиотеки
    :param book_title: Название книги
    :return: None
    """
    followers = models.Follower.objects.all()
    data = f'Добавлена новая книга {book_title}'
    send_mail('Пополнение коллекции книг', data, settings.EMAIL_HOST_USER,
              [follower.email for follower in followers], fail_silently=False)