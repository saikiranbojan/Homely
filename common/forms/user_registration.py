from django import forms
from homely.models import BaseUser

class UserRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = False


    class Meta:
        model = BaseUser
        fields = ('email', 'name','is_staff', 'is_activated')

