# from rest_framework import serializers
# from app.models import User
#
# from chat.models import Room, Chat
#
#
# class UserSerializer(serializers.ModelSerializer):
#     """Сериализация пользователя"""
#     class Meta:
#         model = User
#         fields = ("id", "username")
#
#
# class RoomSerializers(serializers.ModelSerializer):
#     """Сериализация комнат чата"""
#     creator = UserSerializer()
#     invited = UserSerializer(many=True)
#
#     class Meta:
#         model = Room
#         fields = ("id", "creator", "invited", "date")
#
#
# class ChatSerializers(serializers.ModelSerializer):
#     """Сериализация чата"""
#     user = UserSerializer()
#
#     class Meta:
#         model = Chat
#         fields = ("user", "text", "date")
#
#
# class ChatPostSerializers(serializers.ModelSerializer):
#     """Сериализация чата"""
#     class Meta:
#         model = Chat
#         fields = ("room", "text")