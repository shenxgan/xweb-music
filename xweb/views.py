import os
import subprocess
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import VolumeSerializer


class Volume(GenericAPIView):
    queryset = []
    serializer_class = VolumeSerializer

    def get(self, request, format=None):
        """获取当前音量"""
        status, output = subprocess.getstatusoutput('amixer sget PCM | awk -F"[][]" \'/dB/ { print $2 }\'')
        volume = output.rstrip('%') if status == 0 else None
        return Response(volume)

    def post(self, request, format=None):
        """调节音量"""
        serializer = VolumeSerializer(data=self.request.data)
        if serializer.is_valid():
            volume = serializer.validated_data['volume']
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        volume = self.request.POST.get('volume')
        cmd = 'amixer sset PCM {volume}%'.format(volume=volume)
        os.system(cmd)
        return Response(volume)
