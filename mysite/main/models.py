from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
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
    phone_number = models.CharField("Номер телефона", max_length=15, null=False, blank=False)

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

class Service(models.Model):
    name = models.CharField("Имя Услуги", max_length=255,)
    price = models.FloatField("Цена" )


class Master(models.Model):
    user = models.OneToOneField(CustomUser,
    on_delete=models.CASCADE,)
    services = models.ManyToManyField(Service)
    # schedule = models.


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

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
    

class TypesOfServices(models.Model):
    CATEGORY = (
        ("Men's haircut", "Мужская стрижка"),
        ("Women's haircut", "Женская стрижка"),
        ("Children's haircut","Детская  стрижка"))
    name = models.CharField(max_length=200, null=False, )
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True,choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ("В ожиданий","В ожиданий"),
        ("Выполнено","Выполнено")
    )
    customer = models.ForeignKey(CustomUser,null=True, on_delete= models.SET_NULL)
    type_of_service = models.ForeignKey(TypesOfServices, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(default=timezone.now,null=True,)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    times_pick = models.DateTimeField(null=True)
    # df