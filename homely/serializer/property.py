from rest_framework import serializers
from homely.models import Property


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('property_name', 'created_on', 'available', 'rent')

class PropertyAvailability(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()

    def get_owner(self,obj):
        return obj.user.email

    class Meta:
        model = Property
        fields = ('owner', 'property_name', 'available', 'rent')

