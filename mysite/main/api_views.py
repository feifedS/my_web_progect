from rest_framework.generics import ListAPIView, GenericAPIView, ListCreateAPIView
from .serializers import  *
from rest_framework.generics import ListAPIView

from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated
# class ServicesListView(ListAPIView):
#     model = 


# class LoginAPI(generics.GenericAPIView):
#     serializer_class = CustomUserSerializer

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is None:
#             return Response({'error': 'Invalid credentials'})
#         return Response({
#             "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
#             "token": Token.objects.create(user=user).key
#         })
    
class PublisherView(ListAPIView):
    serializer_class = PublisherSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

class OrderApi(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

class TypesOfServicesApi(ListAPIView):
    serializer_class = TypesOfServicesSerializer
    queryset = TypesOfServices.objects.all()
    permission_classes = [IsAuthenticated]

class CategoryApi(ListAPIView):
    serializer_class = CategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = CustomUserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
#             "token": Token.objects.create(user=user).key
#         })