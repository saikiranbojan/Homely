from rest_framework.authtoken.models import Token

class ResponseInfo(object):
    def __init__(self, user=None, **args):
        self.response = {
                         "isSuccess": args.get('is_success', False),
                         "dataInfo": args.get('data_info', []),
                         "message": args.get('message', "")
                         }
        if user:
             self.response['token'] = self.get_token(user)
             self.response['bkp_key'] = str(user.bkp_key)
        
    def get_fresh_token(self, user):
         Token.objects.filter(user=user).delete()
         return Token.objects.create(user=user)

    def get_token(self, user):
         token_obj = Token.objects.filter(user=user).first()
         token = token_obj or self.get_fresh_token(user)
         return token.key

    def delete_token(self, user):
        token = Token.objects.filter(user=user)
        if token:
            token.delete()
        return True

    def set_new_token(self, user):
        self.delete_token(user)
        return Token.objects.create(user=user)

