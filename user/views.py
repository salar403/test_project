from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.views import Response

from project.services.login_manager import logout_leader, logout_user

from user.permissions import IsAuthenticatedUser, IsAuthenticatedLeader
from user.serializers import CreateImageSerializer, ImageListSerializer, LeaderLoginSerializer, RegisterSerializer, UserListSerializer, UserLoginSerializer
from user.models import Image, User


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class Login(generics.CreateAPIView):
    serializer_class = UserLoginSerializer


class Logout(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedUser]
    
    def delete(self, request, *args, **kwargs):
        data = logout_user(request)
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class AddImage(generics.CreateAPIView):
    permission_classes = [IsAuthenticatedUser]
    serializer_class = CreateImageSerializer
    parser_classes = [MultiPartParser]


class LeaderLogin(generics.CreateAPIView):
    serializer_class = LeaderLoginSerializer


class LeaderLogout(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedLeader]

    def delete(self, request, *args, **kwargs):
        data = logout_leader(request)
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class GetUserList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedLeader]
    serializer_class = UserListSerializer

    def get_queryset(self):
        return self.request.leader.users.all()
       

class GetImageList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedLeader]
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user__leader_id = self.request.leader.id)


class GetUserImages(generics.ListAPIView):
    permission_classes = [IsAuthenticatedLeader]
    serializer_class = ImageListSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["pk"])
        return Image.objects.filter(user__leader_id = self.request.leader.id, user_id=user.id)
