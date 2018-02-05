from rest_framework import serializers

from homely.models import BaseUser



class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = ('name', 'date_of_join', 'email')
