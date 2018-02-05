from common.custom_validation import ValidationError
from common.views.baseviews import AuthenticatedAPIView
from rest_framework.response import Response

from homely.serializer.property import PropertyAvailability
from homely.models import Property
class PropertyAvalilabilityView(AuthenticatedAPIView):
    """
    View for Property Availability.
    """

    def get(self, request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        properties = Property.objects.filter(available=True).exclude(user=user_profile)


        data = PropertyAvailability(properties).data

        self.response['isSuccess'] = True
        self.response['dataInfo'] = data
        self.response['message'] = 'Account data fetched successfully'
        return Response(self.response)
