from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#models
class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email=self.normalize_email(email), 
            phone_number = phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            phone_number,
            password=password, 
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=25)
    last_name = models.CharField(verbose_name="last name", max_length=25)
    phone_number = models.CharField(verbose_name="phone number", max_length=120, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin