from rest_framework import serializers


class MusicSerializer(serializers.Serializer):
    name = serializers.CharField()
