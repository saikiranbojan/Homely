from homely.models.users import BaseUser

class CustomBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = BaseUser.objects.get(username=username)
        except BaseUser.MultipleObjectsReturned:
            return None
        except BaseUser.DoesNotExist:
            return None

        if getattr(user, 'is_active') and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return BaseUser.objects.get(pk=user_id)
        except BaseUser.DoesNotExist:
            return None
