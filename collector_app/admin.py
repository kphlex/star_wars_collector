from django.contrib import admin
from .models import Starships, Planets, People

admin.site.register(People)
admin.site.register(Starships)
admin.site.register(Planets)
