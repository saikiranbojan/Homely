from common.custom_validation import ValidationError
from common.views.baseviews import AuthenticatedAPIView
from rest_framework.response import Response

from homely.models import Property, Reservation ,BaseUser
class PropertyReservationView(AuthenticatedAPIView):
    """
    View for Property Reservation.
    """

    def post(self, request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        property_name = request.data.get('property_name',None)
        owner = request.data.get('owner',None)

        if not property_name:
            self.response['message'] = "property name not given"
            raise ValidationError(self.response)

        if not owner:
            self.response['message'] = "owner email id not given"
            raise ValidationError(self.response)

        if owner is user_profile.email:
            self.response['message'] = "You cannot buy your own property"
            raise ValidationError(self.response)



        property = Property.objects.filter(available=True, property_name=property_name).first()

        if not property:
            self.response['message'] = "property not found"
            raise ValidationError(self.response)

        user = BaseUser.objects.filter(email=owner).first()
        if not user:
            self.response['message'] = "owner not found"
            raise ValidationError(self.response)

        obj,created = Reservation.objects.get_or_create(buyer=user,
                                                        property=property)
        reservation = obj or created
        reservation.save()
        property.available = False
        property.save()

        self.response['isSuccess'] = True
        self.response['message'] = 'Reservation done successfully'
        return Response(self.response)
