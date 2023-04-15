from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TypesOfServicesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = TypesOfServices
        fields = ('id','name','price','category','description','tags')

class BarberSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = "__all__"

class BookingSerilizer(serializers.ModelSerializer):
    class Meta: 
        model = Booking
        fields = "__all__"
