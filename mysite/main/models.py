from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager


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
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class Gender(models.Model):
    name = models.CharField("Пол", max_length=1, blank=False, null=False, default="М")


class CustomUser(User):
    phone_number = models.CharField("Номер телефона", max_length=11, null=False, blank=False)

    age = models.DateField("Дата рождения", null=False, blank=False)

    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
