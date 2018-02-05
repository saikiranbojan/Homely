from common.custom_validation import ValidationError
from common.views.baseviews import AuthenticatedAPIView
from rest_framework.response import Response
from common.viewmodels import ResponseInfo
from django.contrib.auth import logout


class LogOutAPI(AuthenticatedAPIView):
    """
    View for user logout.
    """

    def post(self, request):

        user_profile = request.user

        if not user_profile:
            self.response['message'] = "Please ensure you have send the correct token"
            raise ValidationError(self.response)

        try:
            logout(request)
            try:
                ResponseInfo().delete_token(user_profile)
            except:
                pass
        except ValidationError as error:
            self.response['isSuccess'] = False
            self.response['message'] = "You are already logged out"
            raise ValidationError(self.response)

        self.response['isSuccess'] = True
        self.response['message'] = 'Logged out successfully'
        return Response(self.response)
