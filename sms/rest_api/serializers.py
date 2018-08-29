from django.db import transaction
from django.contrib.auth.models import User

from rest_framework import serializers

from sms.models import *


class MobileMessageSerializer(serializers.Serializer):
    app_id = serializers.IntegerField(required=False, min_value=1)
    send_to = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=2048)


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff')

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Application Serializer
    """

    class Meta:
        model = Application
        fields = ('id', 'name', 'max_limit', 'status', 'created_at')
        read_only_fields = ('id', 'created_at',)
