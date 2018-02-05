from rest_framework.response import Response

from common.custom_validation import ValidationError
from common.services.ejabberd import EjabberdClientAPI
from common.viewmodels import ResponseInfo
from common.views.baseviews import BaseAPIView
from homely.forms.user_registration import UserRegistrationForm
from homely.models import BaseUser
from homely.models.activation import UserActivation
from django.conf import settings as conf
from django.core.validators import EmailValidator


class SignUpView(BaseAPIView):
    """
    View for user sign up
    """

    def post(self, request):
        email_validator = EmailValidator()
        self.email = request.POST.get('email', None)
        self.password = request.POST.get('password', None)
        response = ResponseInfo().response
        if not self.password:
            response['message'] = 'password is mandatory'
            raise ValidationError(response)
        if not self.email:
            response['message'] = 'email is mandatory'

        try:
            email_validator(self.email)
        except Exception as error:
            response['message'] = str(error.args)
            raise ValidationError(response)

        post_data = request.POST.copy()

        if self.check_already_registered_user():
            response['message'] = "You have already registered, please login"
            raise ValidationError(response)

        try:
            existing_user = UserActivation.objects.filter(email=self.email).first()
            user_form = UserRegistrationForm(post_data, instance=existing_user)

            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.save()
                self.send_otp(new_user)

            else:
                errors = dict(user_form.errors.items())
                keys = list(errors.keys())
                response['message'] = "".join(
                    [' '.join(keys[0].split('_')).capitalize(), " : ", list(errors.values())[0][0]])
                raise ValidationError(response)
        except ValidationError as error:
            response['isSuccess'] = False
            response['message'] = str(error.args)
            return Response(response)

        response['isSuccess'] = True
        response['message'] = 'Verification code have been send to the given number'
        response['app_base'] = {'xmpp_user_domain': conf.EJABBERD_HOST,
                                'xmpp_group_domain': conf.EJABBERD_CONFERENCE_SERVICE}
        return Response(response)

    def send_otp(self, user):
        user.send_otp()
        return True

    def check_already_registered_user(self):
        status = True if BaseUser.objects.filter(username=self.email).first() else False
        return status
