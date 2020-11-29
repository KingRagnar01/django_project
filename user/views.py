from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
#from .serializers import UserSerializer, RegisterSerializer
from django.shortcuts import render

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
#from knox.views import LoginView as KnoxLoginView


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import filters



from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework import viewsets
from .models import Feeds
from .serializers import FeedSerializer
from rest_framework.decorators import api_view
from . import serializers
from . import models
from . import permis

class CreateTokenView(ObtainAuthToken):
    serializer_class=AuthSerializer
    render_classes=[api_settings.DEFAULT_RENDERER_CLASSES]

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = models.UserProfile
    permission_classes = (permis.UpdateOwnPassword,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def feeds_list(request):
    # GET list of feeds, POST a new feed, DELETE all feeds
    if request.method == 'GET':
        feeds = Feeds.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            feeds = feeds.filter(title__icontains=title)

        feeds_serializer = FeedSerializer(feeds, many=True)
        return JsonResponse(feeds_serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def feed_detail(request, pk):
    # find feeds by pk (id)
    try:
        feed = Feeds.objects.get(pk=pk)
    except Feeds.DoesNotExist:
        return JsonResponse({'message': 'The Feed does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        feeds_serializer = FeedSerializer(feed)
        return JsonResponse(feeds_serializer.data)
    elif request.method == 'PUT':
        feed_data = JSONParser().parse(request)
        feeds_serializer = FeedSerializer(feed, data=feed_data)
        if feeds_serializer.is_valid():
            feeds_serializer.save()
            return JsonResponse(feeds_serializer.data)
        return JsonResponse(feeds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Feeds.objects.all().delete()
        return JsonResponse({
            'message': '{} Feeds are deleted successfully'.format(count[0])
        }, status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(viewsets.ModelViewSet):


    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.object.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permis.UpdateOwnProfile,)
    filter_backends=(filters.SearchFilter,)
    search_fields=('username','email',)

