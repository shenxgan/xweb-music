from rest_framework import serializers


class VolumeSerializer(serializers.Serializer):
    volume = serializers.IntegerField()
