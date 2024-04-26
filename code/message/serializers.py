import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grape.settings")

from message.models import Message,MessageText
from rest_framework import serializers
from user.models import User
from user.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MessageTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageText
        fields = ('role', 'text')


class MessageSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomUser.objects.all())
    texts = MessageTextSerializer(many=True,required=False)

    class Meta:
        model = Message
        fields = ('user_id','uuid', 'image', 'reply','created_datetime','history', 'texts')

    def create(self, validated_data):
        texts_data = validated_data.pop('texts', [])
        message = Message.objects.create(**validated_data)

        for text_data in texts_data:
            MessageText.objects.create(message=message, **text_data)

        return message
    
    def update(self, instance, validated_data):
        texts_data = validated_data.pop('texts', [])

        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if texts_data:
            MessageText.objects.filter(message=instance).delete()
            for text_data in texts_data:
                text = MessageText.objects.create(message=instance, **text_data)

        return instance
