from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    name,
                    surname,
                    phone_number,
                    password=None,
                    is_staff=False,
                    is_admin=False,
                    is_active=True):

        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            phone_number=phone_number,
            staff=is_staff,
            admin=is_admin,
            active=is_active
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, name):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password, name, surname, phone_number):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            name=name,
            surname=surname,
            phone_number=phone_number,
            password=password,
            is_admin=True,
            is_staff=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )

    name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=False)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    phone_number = models.CharField(
        verbose_name='phone number',
        validators=[phone_regex],
        max_length=17,
        blank=False,
        help_text='NUmerpoo'
    )

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone_number']  # Email & Password are required by default.

    def get_full_name(self):
        return self.name + " " + self.surname

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
