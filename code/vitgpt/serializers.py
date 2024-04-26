import os
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grape.settings")
from rest_framework import serializers
from user.serializer import CustomUserSerializer 
from .models import VIT,Image
from user.models import CustomUser

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)
        extra_kwargs = {
            'image': {'required': False}
        }
    

class VITSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomUser.objects.all())
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = VIT
        fields = ('id', 'user_id', 'created_datetime', 'updated_datetime', 'images', 'text')
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        note = VIT.objects.create(**validated_data)
 
        for image_data in images_data:
            Image.objects.create(note=note, **image_data)

        return note

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])

        instance.text = validated_data.get('text', instance.text)
        instance.save()

        # 更新关联的图片
        if images_data:
            Image.objects.filter(note=instance).delete()
            for image_data in images_data:
                image = Image.objects.create(note=instance, **image_data)

        return instance