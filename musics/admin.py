from django.contrib import admin
from .models import Artist, Music, Review
# Register your models here.

admin.site.register(Artist)
admin.site.register(Music)
admin.site.register(Review)