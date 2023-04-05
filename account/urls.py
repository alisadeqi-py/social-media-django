from django.urls import path
from . import views



app_name = 'account'


urlpatterns = [
    path('register/' , views.UserRegisterView.as_view() , name='register'),
    path('login/' , views.UserLoginView.as_view() , name='Userlogin'),
    path('logout/' , views.UserLogoutView.as_view() , name='Userlogout'),
    path('profile/<int:user_id>' , views.UserProfileView.as_view() , name='userprofile'),
    path('follow/<int:user_id>' , views.UserFollowView.as_view() , name='user-follow'),
    path('unfollow/<int:user_id>' , views.UserUnfollowView.as_view() , name='user-unfollow')
]