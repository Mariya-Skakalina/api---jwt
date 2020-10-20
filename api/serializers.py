from rest_framework import serializers
from .models import *


class CitySerializer(serializers.Serializer):
	name = serializers.CharField(max_length=100)


class UserdSerializer(serializers.Serializer):
	login = serializers.CharField(max_length=100)
	password = serializers.CharField(max_length=100)
	name = serializers.CharField(max_length=100, required=False)
	city = CitySerializer

	def create(self, validated_data):
		return User.objects.create(**validated_data)


class AuthSerializer(serializers.Serializer):
	login = serializers.CharField(max_length=100)
	password = serializers.CharField(max_length=100)
	name = serializers.CharField(max_length=100, required=False)


class PostSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=255)
	body = serializers.CharField()
	price = serializers.IntegerField()
	user = UserdSerializer
	city = CitySerializer

	def create(self, validated_data):
		return Post.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.body = validated_data.get('body', instance.body)
		instance.price = validated_data.get('price', instance.price)
		instance.save()
		return instance
