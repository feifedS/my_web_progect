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



class ModelApiList(generics.ListAPIView):
    serializer_class = TypesOfServicesSerializer

    def get_queryset(self):
        queryset = None
        category = self.request.query_params.get('category', None)
        print(category)
        if category:
            new_mark = Category.objects.get(id = category)
            queryset = TypesOfServices.objects.filter(category=new_mark)
        return queryset


class BarberApiList(generics.ListAPIView):
    serializer_class = BarberSerilizer
    def get_queryset(self):
        queryset = Barber.objects.all()
        service = self.request.query_params.get('service', None)
        print(service)
        if service:
            new_mark = TypesOfServices.objects.get(id = service)
            queryset = queryset.filter(services=new_mark)
        return queryset
    
    
class AvailableTimesAjax(generics.ListAPIView):
    def get_queryset(self):
        barber = self.request.GET.get('barber', None) 
        date = self.request.GET.get('date', None) 
        bookings = Booking.objects.filter(barber=barber, date=date).values_list('time', flat=True)
        available_times = []
        start_time = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=9)
        end_time = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=18) 
        while start_time < end_time:
                if start_time.time() not in bookings:
                    available_times.append(start_time.time())
                start_time += datetime.timedelta(minutes=30)
        return  available_times

class BookingApiList(generics.ListAPIView):
    serializer_class = BookingSerilizer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
class BarberApiListGET(generics.ListAPIView):
    serializer_class = BarberSerilizer
    queryset = Barber.objects.all()
    permission_classes = [IsAuthenticated]