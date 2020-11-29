from .views import   ChangePasswordView, feeds_list, feed_detail
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls import include
#from knox import views as knox_views
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('profile',views.UserProfileViewSet)


urlpatterns = [

    #path('api/login/', LoginAPI.as_view(), name='login'),
    #path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    #path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/feeds/', feeds_list, name='feeds_list'),
    path('api/feeds/<pk>', feed_detail),
    path('api/login-token/', views.CreateTokenView.as_view(), name='Token'),
    path('api/',include(router.urls) ),

]
