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

* 현재 musics DB에 있는 파일을 가지고 와서 musics.json 파일을 생성한다.

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

### 2. Serializer(1:N)

```python
# musics/serializers.py
class ArtistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name',]
     
class ArtistDetailSerializers(serializers.ModelSerializer):
    music_set = MusicSerializers(many=True)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'music_set')

# 상속 관계를 이용해서 표현이 가능하다.
class ArtistDetailSerializers(serializers.ModelSerializer):
    music_set = MusicSerializers(many=True)
    class Meta(ArtistSerializers.Meta):
        fields = ArtistSerializers.Meta.fields + ['music_set']
```

* 해당 객체와 1:N 관계인 객체의 인스턴스를 가지고 올 수 있도록 설정이 가능하다.

## 4. API 페이지 구축

### API 홈페이지 구축

```bash
$ pip install -U drf-yasg
```

```python
# settings.py
INSTALLED_APPS = [
   ...
   'drf_yasg',
   ...
]
```

```python
# movies/urls.py

from django.urls import path
from . import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Music API",
      default_version='v1',
      description="Music, Artist",
   ),
)


app_name = 'musics'

urlpatterns = [
    path('musics/', views.index, name='index'),
    path('musics/<int:music_pk>', views.detail, name='detail'),
    path('redoc/', schema_view.with_ui('redoc'), name='api_docs'),
    path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
]
```

* `api/v1/redoc`페이지에서 이미 만들어진 Form을 이용하여 API를 표현한다.
* 혹은 `api/v1/swagger`를 사용해도 된다.

## 5. 리뷰 작성

```python
# musics/serializers.py

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content',]
```

```python
# views.py
# 리뷰 작성
@api_view(['POST'])
def review_create(request, music_pk):
    serializer = ReviewSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):  # 빈 인스턴스가 있다면 예외 처리
        serializer.save(music_id=music_pk)
    return Response({'message': 'review가 등록되었습니다.'})
```

* ModelForm과 비슷하게 사용이 가능하다.

### 6. 수정 및 삭제

```
GET reviews/ 리뷰 목록
POST reviews/ 리뷰 등록하기
GET reviews/1 1번 리뷰 가져오기
PUT reviews/1/ 1번 리뷰 수정하기
DELETE reviews/1/ 1번 리뷰 삭제하기

GUI(Graphic user interface)
그래픽 - 유저와 상호작용하는 인터페이스
CLI(Comment Line Interface)
명령어 인터페이스
API(Application programming interface)
프로그래밍으로 인터페이스
```

```python
# views.py
@api_view(['PUT', 'DELETE'])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':
        serializer = ReviewSerializers(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'review가 성공적으로 수정 되었습니다.'})
    else:
        review.delete()
        return Response({'message': 'review가 성공적으로 삭제 되었습니다.'})
```

