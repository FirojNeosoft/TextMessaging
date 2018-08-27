from rest_framework import serializers


class MobileMessageSerializer(serializers.Serializer):
    send_to = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=2048)

