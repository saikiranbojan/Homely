from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from common.views.baseviews import BaseAPIView
from common.viewmodels import ResponseInfo

class LoginAPI(BaseAPIView):
    """
    View for login user
    """

    def post(self, request):
        self.logged_in_user = None
        self.request = request
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        authenticated = None
        response = ResponseInfo().response

        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            status = 200
            ResponseInfo().set_new_token(authenticated_user)
            response = ResponseInfo(user=authenticated_user).response
            response['isSuccess'] = True
            response['dataInfo'] = []
            response['message'] = "Successfully logged in..!"
            login(request, authenticated_user)
        elif authenticated_user and not authenticated.is_active:
            status = 401
            response['message'] = "Your account has not been activated"
        else:
            status = 401
            response['message'] = "User name or password do not match"

        return Response(response, status=status)
