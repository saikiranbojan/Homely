from django.contrib import admin
from django.db import models

from homely.models import BaseUser, Property


class Reservation(models.Model):


    buyer  = models.ForeignKey(BaseUser)
    property = models.ForeignKey(Property)

    def __unicode__(self):
        return self.buyer.name

admin.site.register(Reservation)