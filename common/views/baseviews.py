from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.versioning import AcceptHeaderVersioning
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.views import APIView
from common.custom_validation import ValidationError

from common.viewmodels import ResponseInfo


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if not auth:
        auth = request.GET.get('token', "")
        if auth:
            auth = 'Token ' + auth
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class BaseAPIView(APIView):
    versioning_class = AcceptHeaderVersioning

    def __init__(self, **kwargs):
        super(BaseAPIView, self).__init__(**kwargs)


class CustomTokenAuthentication(TokenAuthentication):
    """
    Extending token authentication,
    now you can pass tokens as GET parameter
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(('Session expired. Please login again'))
            # raise exceptions.AuthenticationFailed(('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(('User inactive or deleted.'))

        return (token.user, token)



class AuthenticatedAPIView(APIView):
    """
    Parent class of all authenticated views,
    token authentication and URL Path versioning is used
    """
    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    versioning_class = AcceptHeaderVersioning

    def __init__(self, **kwargs):
        super(AuthenticatedAPIView, self).__init__(**kwargs)
        self.response = ResponseInfo().response
