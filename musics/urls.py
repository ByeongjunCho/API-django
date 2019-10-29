from django.urls import path
from . import views
app_name = 'musics'

urlpatterns = [
    path('musics/', views.index, name='index'),
    path('musics/<int:music_pk>', views.detail, name='detail'),
]
