from django.contrib import admin

from src.apps.topics import models

admin.site.register(models.Topic)
admin.site.register(models.Message)
admin.site.register(models.Subscription)
