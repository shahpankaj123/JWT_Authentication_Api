from django.urls import path
from .views import UserRegisterView,UserLoginView,Profileview

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('Userdetail/',Profileview.as_view())
]