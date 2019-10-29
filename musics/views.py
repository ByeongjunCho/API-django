from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Music
from .serializers import MusicSerializers
# Create your views here.

@api_view(['GET']) # HTTP method
def index(request):
    musics = Music.objects.all()
    serializer = MusicSerializers(musics, many=True) # QuerySet
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    serializer = MusicSerializers(music)
    return Response(serializer.data)