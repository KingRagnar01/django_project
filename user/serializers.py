from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feeds
from . import models

# User Serializer
""" class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user """


class ChangePasswordSerializer(serializers.Serializer):
    model = models.UserProfile

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeds
        fields = (
            'id',
            'title',
            'description',
            'image'
        )

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model=models.UserProfile
        fields=('id','email','username','image','password')
        extra_kwargs={'password':{'write_only':True}}

    def Create(self,validated_data):


        user=models.UserProfile(
            email=validated_data['email'],
            name=validated_data['username'],
            image=validated_data['image']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
