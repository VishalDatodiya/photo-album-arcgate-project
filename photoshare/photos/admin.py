from django.contrib import admin

from photos.models import Category, Photo, User


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Photo)
