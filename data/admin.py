# admin.py

from django.contrib import admin
from .models import APIMethod, APIMethodModifier, SearchLog, Comment, Rating, Thread, User

admin.site.register(APIMethod)
admin.site.register(APIMethodModifier)
admin.site.register(SearchLog)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Thread)
admin.site.register(User)