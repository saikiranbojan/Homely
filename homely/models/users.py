
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.contrib import admin
from django.utils import timezone


class BaseUser(AbstractUser):
    email_regex = EmailValidator()

    name = models.CharField(max_length=50, blank=False, null=False, default='homely user')
    date_of_join = models.DateField(auto_now_add=True)
    is_activated = models.BooleanField(default=False)
    email = models.EmailField(null=False,blank=False, validators=[email_regex])
    username = models.CharField(validators=[email_regex], null=False, blank=False)

    def __unicode__(self):
        return self.username

admin.site.register(BaseUser)
