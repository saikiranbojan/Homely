from django import forms
from homely.models import UserActivation

class UserRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = False


    class Meta:
        model = UserActivation
        fields = ('email', 'password','name')

