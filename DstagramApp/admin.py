from django.contrib import admin
from .models import User, Photo, Comment

admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Comment)
