from .models import User
from rest_framework import serializers


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
