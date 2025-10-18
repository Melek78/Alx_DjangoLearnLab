from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']

class FollowActionSerializer(serializers.Serializer):
    target_user_id = serializers.IntegerField()
class UserSerializer(serializers.ModelSerializer):
    following = UserShortSerializer(many=True, read_only=True)
    followers = UserShortSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'following', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
            user = get_user_model().objects.create_user(
                username=validated_data['username'],
                email= validated_data['email'],
                password= validated_data['password']
            )
            Token.objects.create(user=user)
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid Credentials")