from .models import User
from rest_framework import serializers
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError

from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','tc','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password donot match')

        return attrs

    def create(self, validated_data):
       return  User.objects.create_user(**validated_data)   

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields=['email','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','name']

class UserchangepasswordSerializer(serializers.ModelSerializer):
    password= serializers.CharField(style={'input_type':'password'},write_only=True)  
    password1= serializers.CharField(style={'input_type':'password'},write_only=True) 
    

    class Meta:
        model=User
        fields=['password','password1']

    def validate(self, attrs):
        password=attrs.get('password')
        password1=attrs.get('password1')
        user=self.context.get('user')
        if password != password1:
            raise serializers.ValidationError('Password and Confirm Password donot match')
        user.set_password(password)
        user.save()

        return attrs 
            
class UserSendMailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print(token)
            link='http://127.0.0.1:8000/api/user/reset/'+uid+'/'+token
            print(link)
            return attrs
        else:
            raise serializers.ValidationError('Email Not Registered')

class UserPasswordResetSerializer(serializers.Serializer):
    password= serializers.CharField(style={'input_type':'password'},write_only=True)  
    password1= serializers.CharField(style={'input_type':'password'},write_only=True) 
    
    class Meta:
        fields=['password','password1']

    def validate(self, attrs):
        password=attrs.get('password')
        password1=attrs.get('password1') 

        if password != password1:
            raise serializers.ValidationError('Password and Confirm Password donot match')
        
        uid=self.context.get('uid')
        token=self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user=User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is not Valid or Expired') 
        
        user.set_password(password)
        user.save()
        return attrs


    
    