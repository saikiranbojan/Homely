from common.custom_validation import ValidationError
from common.views.baseviews import AuthenticatedAPIView
from rest_framework.response import Response
from homely.models import BaseUser
from homely.serializer.user import SimpleUserSerializer

class MyAccountView(AuthenticatedAPIView):
    """
    View for operations on an account.
    """

    def get(self, request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)


        data = SimpleUserSerializer(user_profile).data
        self.response['isSuccess'] = True
        self.response['dataInfo'] = data
        self.response['message'] = 'Account data fetched successfully'
        return Response(self.response)

    def patch(self,request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        name = request.data.get('name',None)
        if name:
            user_profile.name = name
            user_profile.save()

        self.response['isSuccess'] = True
        self.response['message'] = 'Account updated successfully'
        return Response(self.response)

    def delete(self,request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        user_profile.is_active = False
        user_profile.save()

        self.response['isSuccess'] = True
        self.response['message'] = 'Account deactivated successfully'
        return Response(self.response)
