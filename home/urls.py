from django.urls import path
from .views import UserRegisterView,UserLoginView,Profileview,UserchangepasswordView,UserSendMailView,UserPasswordResetView

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('Userdetail/',Profileview.as_view()),
    path('changepassword/',UserchangepasswordView.as_view()),
    path('sendmail/',UserSendMailView.as_view()),
    path('reset/<uid>/<token>',UserPasswordResetView.as_view())
]