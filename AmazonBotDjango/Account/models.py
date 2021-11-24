from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Email neded")
        if not username:
            raise ValueError("Username neded")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username, 
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(verbose_name="email", unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last logging", auto_now=True)

    is_admin = models.BooleanField(verbose_name="is admin", default=False)
    is_active = models.BooleanField(verbose_name="is active", default=True)
    is_staff = models.BooleanField(verbose_name="is staff", default=False)
    is_superuser = models.BooleanField(verbose_name="is super", default=False)

    email_notification = models.EmailField(
        verbose_name="email notification", null=True, blank=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
