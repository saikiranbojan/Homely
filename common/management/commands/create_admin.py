from django.core.management import BaseCommand
from homely.models import BaseUser
from common.forms.user_registration import UserRegistrationForm
class Command(BaseCommand):
    help = "To admin user"
    #pass parameters as dictionary
    def handle(self, *args, **options):
        admin = BaseUser.objects.filter(email=options.get('email',None)).first()
        options['is_staff']  = True
        options['is_activated']  = True
        reg_form = UserRegistrationForm(options,instance=admin)
        if reg_form.is_valid():
            obj, created = BaseUser.objects.get_or_create(name=options.get('name',None),email=options['email'],is_activated=True, is_staff=True,username=options['email'])
            user = obj or created
            user.set_password(options.get('password',None))
            user.save()
            print('admin created succesfully')
        else:
            print('given user data is not valid')