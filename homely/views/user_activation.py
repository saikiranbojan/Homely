from rest_framework.response import Response
from common.custom_validation import ValidationError
from common.viewmodels import ResponseInfo
from common.views.baseviews import BaseAPIView
from homely.models import BaseUser
from homely.models import UserActivation





class UserActivationView(BaseAPIView):
    """
    View for activating user
    """

    def post(self, request):

        activation_code = request.POST.get('activation_code', None)
        self.email = request.POST.get('email', None)
        response = ResponseInfo().response


        self.username = self.email

        if not activation_code:
            response['message'] = "Please provide your activation code"
            raise ValidationError(response)

        user_activation = UserActivation.objects.filter(email=self.email).first()

        if not user_activation:
            response['message'] = "Incorrect email"
            raise ValidationError(response)

        if not self.is_activated(user_activation, activation_code):
            response['message'] = "You have entered an incorrect activation code"
            raise ValidationError(response)

        try:
            if self.email_taken_by_registered_user(user_activation):
                response['message'] = "This email is already taken by another user"
                raise ValidationError(response)

            base_user = self.create_base_user(user_activation)
            user_activation.delete()
        except ValidationError as error:
            if error.args:
                response['message'] = str(error.args)
            else:
                response['message'] = "Can't save the details, please try later"
            response['reason'] = str(error.args)
            raise ValidationError(response)

        response = ResponseInfo(user=base_user).response
        response['isSuccess'] = True
        response['message'] = 'User verified successfully'
        return Response(response)

    def is_activated(self, user_activation, activation_code):
        is_activated = False
        if activation_code == str(user_activation.otp):
            is_activated = True
        return is_activated

    def create_base_user(self, activated_user):
        obj, created = BaseUser.objects.update_or_create(username=self.email,
                                                         defaults={'email': activated_user.email,
                                                                   'is_activated': True})
        user = obj or created
        user.set_password(activated_user.password)
        user.save()
        return user

    def email_taken_by_registered_user(self, user_activation_object):
        status = True if BaseUser.objects.filter(email=user_activation_object.email).first() else False
        return status
