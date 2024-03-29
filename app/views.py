from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(request.user.id)
        user = User.objects.get(pk=request.user.id)
        if user.is_staff:
            app = ApplicationModel.objects.all()
            serializer = ApplicationListSerializer(app, many=True)
            return Response(serializer.data)
        else:
            app = ApplicationModel.objects.filter(author=request.user.id)
            serializer = ApplicationListSerializer(app, many=True)
            return Response(serializer.data)


class ApplicationView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        print(request.user.id)
        app = ApplicationModel.objects.get(pk=pk)
        serializer = ApplicationSerializer(app, )
        return Response(serializer.data)


class UsersApplicationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        app = ApplicationModel.objects.filter(author=request.user.id)
        serializer = ApplicationListSerializer(app, many=True)
        return Response(serializer.data)


class AddApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddUserView(APIView):
#
#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetChatMessages(APIView):
    """Получить все сообщения из чата"""

    def get(self, request, pk):
        massages = Chat.objects.filter(app=pk)
        serializer = ChatGetSerializer(massages, many=True)
        return Response({"data": serializer.data})


class GetMyName(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})


class SendMessageView(APIView):
    """Диалог чата, сообщение"""
    permission_classes = [permissions.IsAuthenticated, ]

    # permission_classes = [permissions.AllowAny, ]

    # def get(self, request):
    #     room = request.GET.get("room")
    #     chat = Chat.objects.filter(room=room)
    #     serializer = ChatSerializers(chat, many=True)
    #     return Response({"data": serializer.data})

    def post(self, request):
        # room = request.data.get("room")
        dialog = ChatPostSerializers(data=request.data)
        print(request.user)
        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)

# class AddUsersRoom(APIView):
#     """Добавление юзеров в комнату чата"""
#
# def get(self, request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)
#
# def post(self, request):
#     room = request.data.get("room")
#     user = request.data.get("user")
#     try:
#         room = Room.objects.get(id=room)
#         room.invited.add(user)
#         room.save()
#         return Response(status=201)
#     except:
#         return Response(status=400)
