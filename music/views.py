import os

from django.conf import settings
# from django.shortcuts import render
# from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
# from rest_framework.schemas import AutoSchema
# from rest_framework.schemas import ManualSchema

from .serializers import MySerializer
from utils.kugou import search


@api_view(http_method_names=['GET'])
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    data = {'key_dict': {'k': 'v', 'k2': 'v2'}, 'key_list': [i for i in range(9)], 'key_str': 'value'}
    return Response(data)


class Music(GenericAPIView):
    queryset = []
    serializer_class = MySerializer

    def dispatch(self, request, *args, **kwargs):
        mp3_path = os.path.join(settings.STATIC_ROOT, 'mp3')
        self.songs = os.listdir(mp3_path)
        return super(Music, self).dispatch(request, *args, **kwargs)

    def get(self, request, format=None):
        """获取歌曲列表"""
        print(self.songs)
        return Response(self.songs)

    def post(self, request, format=None):
        """查找/下载歌曲"""
        serializer = MySerializer(data=self.request.data)

        if serializer.is_valid():
            name = serializer.validated_data['name']
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        print(name)
        print(request.POST)
        print(request.data)
        # name = self.request.POST.get('name')
        search_songs = []
        for song in self.songs:
            if name in song:
                search_songs.append(song)
        if not search_songs:
            song = search(name)
            search_songs.append(song)
        return Response(search_songs)


class MusicMethod(APIView):
    def patch(self, request, name, format=None):
        """播放歌曲"""
        context = {
            'name': name,
        }
        return Response(context)

    def delete(self, request, name, format=None):
        """删除歌曲"""
        print(self.songs)
        return Response(self.songs)


class MusicLyr(APIView):
    def get(self, request, name, format=None):
        """获取歌词"""
        print(request.data)
        lyr = os.path.join(settings.STATIC_ROOT, 'lyric', name.replace('mp3', 'lyr'))
        if os.path.isfile(lyr):
            with open(lyr, 'r') as f:
                lyrics = f.read()
        else:
            lyrics = '未找到歌词！'
        context = {
            'lyrics': lyrics,
            'name': name,
        }
        return Response(context)

    def delete(self, request, name, format=None):
        """删除歌词"""
        print(request.data)
        lyr = os.path.join(settings.STATIC_ROOT, 'lyric', name.replace('mp3', 'lyr'))
        if os.path.isfile(lyr):
            pass
            msg = '删除成功'
        else:
            msg = '未找到歌词！'
        context = {
            'msg': msg,
            'name': name,
        }
        return Response(context)
