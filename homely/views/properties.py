from common.custom_validation import ValidationError
from common.views.baseviews import AuthenticatedAPIView
from rest_framework.response import Response
from homely.models.properties import Property
from homely.serializer.property import PropertySerializer
from homely.forms.property import PropertyForm

class PropertiesView(AuthenticatedAPIView):
    """
    View for operations on properties.
    """

    def get(self, request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        properties = user_profile.user_properties.all()

        data = PropertySerializer(properties, many=True).data



        self.response['isSuccess'] = True
        self.response['dataInfo'] = data
        self.response['message'] = 'properties fetched successfully'
        return Response(self.response)

    def post(self,request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        property_name = request.data.get('property_name',None)
        property_data = request.data.copy()
        property_data['user'] = user_profile.id
        existing_property = user_profile.user_properties.filter(property_name=property_name).first()
        property_form = PropertyForm(property_data,instance=existing_property)
        if property_form.is_valid():
            property_form.save(commit=False)
        else:
            self.response['message'] = property_form.errors
            raise ValidationError(self.response)

        self.response['isSuccess'] = True
        self.response['message'] = 'Property added successfully'
        return Response(self.response)


    def patch(self,request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        property_name = request.data.get('property_name',None)
        if not property_name:
            self.response['message'] = "property not found"
            raise ValidationError(self.response)
        property_data = request.data.copy()
        existing_property = user_profile.user_properties.filter(property_name=property_name).first()
        if not existing_property:
            self.response['message'] = "property not found"
            raise ValidationError(self.response)
        property_form = PropertyForm(property_data,instance=existing_property)
        if property_form.is_valid():
            property_form.save(commit=False)
        else:
            self.response['message'] = property_form.errors
            raise ValidationError(self.response)


        self.response['isSuccess'] = True
        self.response['message'] = 'Property updated successfully'
        return Response(self.response)

    def delete(self,request):
        user_profile = request.user
        if not user_profile:
            self.response['message'] = "User not found"
            raise ValidationError(self.response)
        property_name = request.data.get('property_name',None)
        if not property_name:
            self.response['message'] = "property name not given"
            raise ValidationError(self.response)
        existing_property = user_profile.user_properties.filter(property_name=property_name).first()
        if not existing_property:
            self.response['message'] = "property not found"
            raise ValidationError(self.response)

        if existing_property.available is False:
            self.response['message'] = "property holded"
            raise ValidationError(self.response)

        existing_property.delete()


        self.response['isSuccess'] = True
        self.response['message'] = 'Account deactivated successfully'
        return Response(self.response)
