from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from apps.core.models import UniqueID,TimeStampedModel
from django.conf import settings
from apps.core.managers import SoftDeleteManager
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message='Phone number must contain 9-15 digits, optionally starting with +.',
)


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)  # хеширует пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # логин по email, username не нужен
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, validators=[phone_validator], blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Mandate(UniqueID, TimeStampedModel):
    steuerberater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='mandates_as_steuerberater')
    mandant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='mandates_as_mandant')
    is_active = models.BooleanField(default=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def __str__(self):
        return f"{self.steuerberater.email} → {self.mandant.email}"

    class Meta:
        unique_together = ('mandant', 'steuerberater')