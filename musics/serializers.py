# json 파일로 변형하기 위한 serializer설정
from rest_framework import serializers
from .models import Music

class MusicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist_id',)