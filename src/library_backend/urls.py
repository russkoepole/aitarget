from django.urls import path

from . import views

app_name = 'library_backend'

urlpatterns = [
    # Маршруты модели Book
    path('books/', views.BookListView.as_view(), name='api-list-books'),
    path('books/<uuid:uuid>/', views.BookDetailView.as_view(), name='api-books-detail'),

    # Маршруты модели Authors
    path('authors/', views.AuthorListView.as_view(), name='api-list-authors'),
    path('authors/<uuid:uuid>/', views.AuthorDetailView.as_view(), name='api-authors-detail'),

    # Маршруты модели Follower
    path('followers/', views.FollowerListView.as_view(), name='api-followers-list'),
    path('followers/<uuid:uuid>/', views.FollowerDetailView.as_view(), name='api-followers-detail'),

    # Маршруты модели User
    path('users/', views.UserListView.as_view(), name='api-users-list'),
    path('users/<uuid:uuid>/', views.UserDetailView.as_view(), name='api-users-detail'),

    # Маршруты модели Language
    path('languages/', views.LanguageListView.as_view(), name='api-languages-list'),
    path('languages/<int:id>/', views.LanguageDetailView.as_view(), name='api-language-detail'),

    # Маршруты модели Genre
    path('genres/', views.GenreListView.as_view(), name='api-genres-list'),
    path('genres/<int:id>/', views.GenreDetailView.as_view(), name='api-genres-detail'),

]