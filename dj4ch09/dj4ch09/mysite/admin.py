from django.contrib import admin
from mysite import models

admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Vote)