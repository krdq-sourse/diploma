# from django.db.models import Q
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions
#
# from app.models import User
#
# from chat.models import Room, Chat
# from chat.serializers import (RoomSerializers, ChatSerializers, ChatPostSerializers,  UserSerializer)
#
#
# class Rooms(APIView):
#     """Комнаты чата"""
#     permission_classes = [permissions.IsAuthenticated, ]
#
#     def get(self, request):
#         # print("delo pahnit huevo")
#         rooms = Room.objects.filter(Q(creator=request.user) | Q(invited=request.user))
#         serializer = RoomSerializers(rooms, many=True)
#         #
#         # print(serializer)
#         # print("delo pahnet jopoi")
#         return Response({"data": serializer.data})
#
#     def post(self, request):
#         Room.objects.create(creator=request.user)
#         return Response(status=201)
#
#
# class Dialog(APIView):
#     """Диалог чата, сообщение"""
#     permission_classes = [permissions.IsAuthenticated, ]
#     # permission_classes = [permissions.AllowAny, ]
#
#     def get(self, request):
#         room = request.GET.get("room")
#         chat = Chat.objects.filter(room=room)
#         serializer = ChatSerializers(chat, many=True)
#         return Response({"data": serializer.data})
#
#     def post(self, request):
#         # room = request.data.get("room")
#         dialog = ChatPostSerializers(data=request.data)
#         if dialog.is_valid():
#             dialog.save(user=request.user)
#             return Response(status=201)
#         else:
#             return Response(status=400)
#
#
# class AddUsersRoom(APIView):
#     """Добавление юзеров в комнату чата"""
#     def get(self, request):
#         print("addUserRoom view (GET method) beginning")
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         print("addUserRoom view (GET method) ending")
#         return Response(serializer.data)
#
#     def post(self, request):
#         room = request.data.get("room")
#         user = request.data.get("user")
#         try:
#             room = Room.objects.get(id=room)
#             room.invited.add(user)
#             room.save()
#             return Response(status=201)
#         except:
#             return Response(status=400)