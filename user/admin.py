from django.contrib import admin
from .models import Feeds
from . import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(Feeds)
