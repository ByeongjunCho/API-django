# Django API

## 1. 환경 설정

### 1. djangorestframework 환경구축

```bash
$ pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    'rest_framework',
]
```

## 2. Model 구축

```python
# models.py
from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.TextField()

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.TextField()

class Review(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    content = models.TextField()
```

### 참고사항

```bash
$ python manage.py dumpdata musics > musics.json
```

* musics.json 파일이 만들어진다.

```bash
$ python manage.py dumpdata --indent 2 musics > musics.json
```

* musics.json 파일이 만들어진다.(들여쓰기가 있는 상태)

```bash
$ python manage.py loaddata musics.json
```

* `app_name/fextures`에 있는 json파일을 불러와서 데이터베이스에 반영한다.

## 3. Serializer 구축

### 1. Serializer

* ModelForm을 만들던 것처럼 json파일형식을 만들기 위해 serialisers.py를 만들어 사용한다.

```python
# serializers.py
# json 파일로 변형하기 위한 serializer설정
from rest_framework import serializers
from .models import Music

class MusicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist_id',)
```

```python
# views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Music
from .serializers import MusicSerializers
# Create your views here.

@api_view(['GET']) # HTTP method
def index(request):
    musics = Music.objects.all()
    serializer = MusicSerializers(musics, many=True) 
    # QuerySet인 경우 many를 추가하여 list로 반환
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    serializer = MusicSerializers(music)
    return Response(serializer.data)
```

* 해당하는 url로 이동하면 json형식으로 데이터를 반환하는 것을 확인할 수 있다.