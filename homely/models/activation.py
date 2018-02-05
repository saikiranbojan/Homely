import random
from django.db import models
from django.utils import timezone
from django.template import loader
from django.conf import settings
from common.mailer import send_email
from common.models import BaseModel
from common.sms import send_sms
from common.custom_validation import ValidationError
from django.core.validators import EmailValidator

class UserActivation(BaseModel):
    """
    User Data Temporary storage for activation
    """
    email_regex = EmailValidator()

    name = models.CharField(max_length=50, default='homely user')
    email = models.EmailField(blank=False, null=False, validators=[email_regex])
    password = models.TextField(blank=False)
    otp = models.PositiveIntegerField(unique=True)
    generated_on = models.DateTimeField()
    is_activated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.otp = self.create_activation_code()
        self.generated_on = timezone.now()
        if self.pk is None:
            self.generated_on = timezone.now()
        return super(UserActivation, self).save(*args, **kwargs)

    def send_otp(self):
        message = 'Homely verification code is :-{}'.format(self.otp)
        if self.email:
            self.send_mail(self.otp)

    def send_mail(self, otp):
        template = loader.get_template('email/otp.html')
        mail_subject = 'Homely OTP'
        html = template.render({'otp': otp, 'site_url': settings.SITE_URL})
        send_email(recipient_list=[self.email], subject=mail_subject, html_message=html, attachments=[])

    def create_activation_code(self):
        expired_otp = UserActivation.objects.filter(generated_on__lte=(timezone.now() - timezone.timedelta(minutes=5))).exclude(email=self.email)
        if expired_otp:
            expired_otp.delete()
        current_otps = [i[0] for i in UserActivation.objects.all().values_list('otp')]

        start = 1000
        end = 9999
        safety_buffer = 9
        if len(current_otps) >= (abs(end-start-safety_buffer)):
            raise ValidationError('Please try again later')
        while True:
            otp = random.randrange(start, end)
            if otp not in current_otps:
                return otp



