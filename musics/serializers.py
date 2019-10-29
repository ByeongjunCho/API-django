# json 파일로 변형하기 위한 serializer설정
from rest_framework import serializers
from .models import Music, Artist, Review

class MusicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist_id',)

class ArtistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name',]

# class ArtistDetailSerializers(serializers.ModelSerializer):
#     music_set = MusicSerializers(many=True)
#     class Meta:
#         model = Artist
#         fields = ('id', 'name', 'music_set')

class ArtistDetailSerializers(serializers.ModelSerializer):
    music_set = MusicSerializers(many=True)
    class Meta(ArtistSerializers.Meta):
        fields = ArtistSerializers.Meta.fields + ['music_set']

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content',]