from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import *
from .serializers import *


class ApplicationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        app = ApplicationModel.objects.all()
        serializer = ApplicationListSerializer(app, many=True)
        return Response(serializer.data)


class AddApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        serializer = AddApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.user_id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)