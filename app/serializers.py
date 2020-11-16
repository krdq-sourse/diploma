from rest_framework import serializers

from .models import *


class ApplicationListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True, many=False)

    class Meta:
        model = ApplicationModel
        fields = "__all__"


class AddApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModel
        fields = "__all__"
