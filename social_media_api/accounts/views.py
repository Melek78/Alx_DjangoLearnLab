from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserShortSerializer
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, GenericAPIView
from django.contrib.auth import get_user_model

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': response.data, 'token': token.key})

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target)
        return Response({'detail': f'Now following {target.username}.'}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(target)
        return Response({'detail': f'Unfollowed {target.username}.'}, status=status.HTTP_200_OK)

class MyFollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = request.user.following.all()
        serializer = UserShortSerializer(users, many=True)
        return Response(serializer.data)

class MyFollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = request.user.followers.all()
        serializer = UserShortSerializer(users, many=True)
        return Response(serializer.data)