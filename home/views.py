from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import UserRegisterSerializer,UserLoginSerializer
from django.contrib.auth import authenticate


class UserRegisterView(APIView):
    def post(self,request,format=None):
        serializer=UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':'Registration successfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                return Response({'msg':'Login successfull'},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg':'Login unsuccessfull'},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'erroe'},status=status.HTTP_400_BAD_REQUEST)    



