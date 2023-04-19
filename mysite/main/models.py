from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
import datetime
from phonenumber_field.modelfields import PhoneNumberField
class Service(models.Model):
    name = models.CharField("Имя Услуги", max_length=255,)
    price = models.FloatField("Цена" )


# class Master(models.Model):
#     user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,)
#     services = models.ManyToManyField(Service)
#     # schedule = models.


class DayOfWeek(models.Model):
    name = models.CharField("Дни недели",max_length=15,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"


class WorkingHours(models.Model):
    name = models.CharField("Время Работы", max_length=20 )


class Rest(models.Model):
    name = models.CharField("Обед", max_length=20 )


class MasterShadow(models.Model):
      day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE, verbose_name="День недели")
      working_hours = models.ForeignKey(WorkingHours,on_delete=models.CASCADE, verbose_name="Время работы")
      rest = models.ForeignKey(Rest,on_delete=models.CASCADE, verbose_name="Обед")


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, email, **extra_fields):
        """
        Create and save a user with the given email and password.
        """

        print("HBFSHJDFBHDSBFHDSBFHJDSBFJSs")
        
        if not email:
            raise ValueError(("The Email must be set"))
        # elif len(password) <=6:
        #     raise ValueError(("Пороль должен быть строго больше 6 символов"))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        group = Group.objects.get(name='customer')
        user.save()
        user.groups.add(group)
        # user.save()
        return user

class Gender(models.Model):
    name = models.CharField("Пол", max_length=1, blank=False, null=False, default="М")

class CustomUser(User):
    phone_number = models.CharField("Номер телефона", max_length=16, null=False, blank=False)
    # phone_number = PhoneNumberField("Номер телефона", null=False, blank=False)
    age = models.DateField("Дата рождения", null=False, blank=False)

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    
    objects = CustomUserManager()
    # role_objects = User()
    CUSTOMER = 1
    MASTER = 2
    # MODER =3
      
    ROLE_CHOICES = (
          (CUSTOMER, 'Customer'),
          (MASTER, 'Master'),
        #   (MODER, 'Moder'),
      )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CUSTOMER)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=200, null=True,)
    def __str__(self):
        return self.name

class TypesOfServices(models.Model):
    
    name = models.CharField(max_length=200, null=False, )
    price = models.FloatField(null=True)
    category = models.ForeignKey(Category,max_length=200, null=True,on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=200, null=True, )

    def __str__(self):
        return self.name

class Barber(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    services = models.ManyToManyField(TypesOfServices, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    service = models.ForeignKey(TypesOfServices, on_delete=models.CASCADE,null=True,default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barber} - {self.customer} - {self.date} - {self.time} - {self.service} - {self.status}"

class Order(models.Model):
    customer = models.ForeignKey(CustomUser,null=True, on_delete= models.SET_NULL)
    type_of_service = models.ForeignKey(TypesOfServices, null=True, on_delete= models.SET_NULL, verbose_name="Виды Сервисов")
    date_created = models.DateTimeField(default=timezone.now,null=True,)
    status = models.ForeignKey(Status,max_length=201, null=True, on_delete=models.CASCADE,default=1)
    times_pick = models.DateTimeField(null=True)

    def __str__(self):
        return self.type_of_service.name

# class AvailableTimeSlot(models.Model):
#     barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     @staticmethod
#     def get_available_time_slots(barber, appointment_date):
#         # Get all time slots for the given barber and date
        

#         # Generate a list of all time slots in 30-minute increments
#         all_time_slots = []
#         start_time = datetime.time(hour=9, minute=0)
#         end_time = datetime.time(hour=18, minute=0)
#         current_time = datetime.datetime.combine(appointment_date, start_time)
#         end_datetime = datetime.datetime.combine(appointment_date, end_time)
#         while current_time <= end_datetime:
#             all_time_slots.append(current_time.time().strftime('%H:%M'))
#             current_time += datetime.timedelta(minutes=30)

#         # Remove any time slots that have already been booked
#         booked_time_slots = Appointment.objects.filter(barber=barber, date=appointment_date).values_list('start_time', flat=True)
#         available_time_slots = [time_slot for time_slot in all_time_slots if time_slot not in booked_time_slots]

#         return available_time_slots
    
# class Appointment(models.Model):
#     barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
  

#     def __str__(self): return f"{self.date} {self.start_time}"