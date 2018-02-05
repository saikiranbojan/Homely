from django.conf.urls import url
from homely.views.login import LoginAPI
from homely.views.logout import LogOutAPI
from homely.views.account import MyAccountView
from .views.signup import SignUpView
from .views.user_activation import UserActivationView
from .views.properties import PropertiesView
from .views.property_availability import PropertyAvailability
from .views.property_reservation import PropertyReservationView

urlpatterns = [
    url(r'^sign-up/$', SignUpView.as_view()),
    url(r'^activate/$', UserActivationView.as_view()),
    url(r'^login/$', LoginAPI.as_view()),
    url(r'^logout/$', LogOutAPI.as_view()),
    url(r'^my-account/$', MyAccountView.as_view()),
    url(r'^property/$', PropertiesView.as_view()),
    url(r'^property-availability/$', PropertyAvailability.as_view()),
    url(r'^reserve-property/$', PropertyReservationView.as_view()),

]
