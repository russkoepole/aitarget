from django.contrib import admin

from . import models

admin.site.register(models.Book)
admin.site.register(models.User)
admin.site.register(models.Follower)
admin.site.register(models.Language)
admin.site.register(models.Genre)
admin.site.register(models.Author)
