from django import forms
from homely.models import Property

class PropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Property, self).__init__(*args, **kwargs)

    class Meta:
        model = Property
        fields = ('user', 'property_name','available', 'rent')

