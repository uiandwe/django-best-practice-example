# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Post
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return str(obj.owner)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user

        return super().create(validated_data)

    class Meta:
        model = Post
        fields = ["id", "message", "created_at", "count", "public", "owner"]
