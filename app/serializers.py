from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }


class ApplicationListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True, many=False)
    responsible_staff = serializers.SlugRelatedField(slug_field="username", read_only=True, )

    class Meta:
        model = ApplicationModel
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True, )
    responsible_staff = serializers.SlugRelatedField(slug_field="username", read_only=True, )

    class Meta:
        model = ApplicationModel
        fields = "__all__"


class AddApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModel
        fields = "__all__"


class GetUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "is_staff"]


# chat
class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class StaffChatSerializer(serializers.ModelSerializer):
    """Сериализация operatora"""

    class Meta:
        model = ApplicationModel
        fields = ("responsible_staff", )


class AuthorChatSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    class Meta:
        model = ApplicationModel
        fields = ("author", )


class RoomSerializers(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    author = AuthorChatSerializer()
    responsible_staff = StaffChatSerializer()

    class Meta:
        model = Room
        fields = ("id", "author", "responsible_staff")


class ChatSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ("user", "text", "date")


class ChatPostSerializers(serializers.ModelSerializer):
    """Сериализация чата"""

    class Meta:
        model = Chat
        fields = ("room", "text")
