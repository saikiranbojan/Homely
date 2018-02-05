from django.contrib import admin
from django.db import models

from homely.models import BaseUser, os
from django.utils import timezone
from datetime import datetime

class Property(models.Model):


    user = models.ForeignKey(BaseUser, related_name='user_properties')
    property_name = models.CharField(max_length=254)
    created_on = models.DateField(auto_now_add=True)
    available = models.BooleanField(default=True)
    rent = models.DecimalField(default=None,null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ["user", "property_name"]

admin.site.register(Property)