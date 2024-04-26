from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import CustomUser
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','last_login']


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model=CustomUser
        fields='__all__'
        depth=1
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username']=validated_data.get('phone')
        user_data['password']=make_password(validated_data.get('validation_code'))
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save
        profile = CustomUser.objects.create(user=user, **validated_data)
        return profile
    
    def update(self, instance, validated_data):
        if validated_data:
            instance.phone = validated_data.get('phone')
            instance.validation_code = validated_data.get('validation_code')
            user_data = validated_data.pop('user')
            user_data['username']=validated_data.get('phone')
            user_data['password']=make_password(validated_data.get('validation_code'))
            User.objects.filter(username=instance.phone).update(**user_data)
            instance.save()
            return instance
        else:
            raise ValidationError('更新数据失败')