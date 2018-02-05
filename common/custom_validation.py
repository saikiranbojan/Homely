from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'

    def __init__(self, detail, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect may errors together, so the
        # details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _force_text_recursive(detail)


def _force_text_recursive(data):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings into plain text.
    """
    if isinstance(data, list):
        ret = [
            _force_text_recursive(item) for item in data
            ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return data
    elif isinstance(data, dict):
        ret = {
            key: _force_text_recursive(value)
            for key, value in data.items()
            }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return data
    return force_text(data)
