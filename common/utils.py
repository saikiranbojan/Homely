from datetime import datetime, timedelta
from random import choice
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from pytz import timezone as pytztz
from rest_framework.fields import DateTimeField
import json
import decimal
import time
import urllib
import uuid

def to_date_obj(date_string):
    for date_fmt in ('%m/%d/%Y', '%m-%d-%y', '%m/%d/%y', '%m-%d-%Y'):
        try:
            return datetime.strptime(date_string, date_fmt)
        except ValueError:
            pass
    raise ValidationError('Invalid date format, please enter in MM/DD/YYYY format')

def format_date(date):
    return date.strftime('%m/%d/%Y')

def to_datetime(timestamp_string, silent_fail=False, tz_info=None):
    for date_fmt in ('%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%s', '%m-%d-%y %H:%M:%s' , '%m/%d/%y %H:%M:%s', settings.COMMON_DATE, '%m/%d/%Y %I:%M:%S %p'):
        try:
            datetime_obj = datetime.strptime(timestamp_string, date_fmt)
            if tz_info:
                datetime_obj = datetime_obj.replace(tzinfo=pytztz(tz_info))
            return datetime_obj
        except (ValueError, TypeError) as e:
            raise ValidationError(e.message)
    if not silent_fail:
        raise ValidationError('Invalid date format, please enter in MM/DD/YYYY hh:mm:ss format')
    else:
        return None
    
def generate_random_string(length=8):
    """
    Generates a random string
    """
    string = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOGthequickbrownfoxjumpsoverthelazydog.-_=$@#!1234567890"
    l = lambda: choice(list(string))
    return ''.join(l() for s in range(length))

def generate_uuid(name):
    return uuid.uuid5(uuid.NAMESPACE_DNS, str(name))



# def send_email(subject, message, recipient_list, fail_silently=True, auth_user=None,
#                auth_password=None, connection=None, html_message=None, attachments=None,
#                reply_to=None
#                ):
#     Mailer().delay(subject=subject, message=message, recipient_list=recipient_list,
#                    fail_silently=fail_silently, auth_user=auth_user, auth_password=auth_password,
#                    connection=connection, html_message=html_message, attachments=attachments,
#                    from_email=settings.EMAIL_FROM_ADDRESS, reply_to=reply_to
#                    )
#     return True

# def is_iterable(obj):
#     iterable = True
#     try:
#         object_iterator = iter(obj)
#     except TypeError, te:
#         iterable = False
#     return iterable

# def encrypt(message, key=None):
#     if not key:
#         key = settings.ENCRYPTION_KEY
#
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CFB, iv)
#     msg = iv + cipher.encrypt(message)
#     return msg.encode("hex")
#
# def decrypt(cipher_text, key=None):
#     if not key:
#         key = settings.ENCRYPTION_KEY
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(key, AES.MODE_CFB, iv)
#     return cipher.decrypt(cipher_text.decode("hex"))[len(iv):]

def day_validator(value):
    if not 1 <= value <= 31:
        raise ValidationError('Invoice Date: Invalid date')

def string_to_int_list(string):
    """
    Convert comma separated values of string of integers to list
    Eg: input  "12, 5,9,   24, qw, ssss"
    output : ["12", "5", "9", "24"] 
    """
    return filter(lambda l: l.isdigit(), map(lambda d: d.strip(), string.split(',')))

def timestamped_filename(prefix, extension):
    params = [prefix] + list(timezone.now().timetuple()) + [extension]
    return r'{0}_{1}{2}{3}{4}{5}{6}{7}{8}{9}.{10}'.format(*params)


def split_name(name):
    """
    Splits a name, returns as first name and last name
    """
    first_name = last_name = ""
    names = filter(lambda t:t.strip(), name.split(' '))
    
    if names:
        first_name = " ".join(names[:-1]) if len(names) > 1 else names[0]
        last_name = names[-1] if len(names) > 1 else "" 
    
    return first_name, last_name

def to_int(obj):
    """
    Converts any object to number,
    return None if conversion fails
    """
    try:
        number = int(obj)
    except:
        number = None
    return number

def decode_number(number):
    return '+' + str(number)

class ZoneDateTimeField(DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(ZoneDateTimeField, self).to_representation(value)




def check_file_extension(self, file_obj, allowed_extensions):
    is_valid_image = True
    
    file_name = str(file_obj)
    dot = file_name.rfind(".")
    extension = file_name[dot + 1:]
    if extension.lower() not in allowed_extensions:
        is_valid_image = False
    return is_valid_image

def geo_code(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = urllib.urlencode({ 'address': address.encode('utf8'), 'key': settings.MAPS_API_KEY})
    try:
        response = json.loads(urllib.urlopen(''.join([url, params])).read())
        lat = response['results'][0]['geometry']['location']['lat']
        lng = response['results'][0]['geometry']['location']['lng']
    except Exception:
        lat = lng = None
    return lat, lng


to_tags = lambda dictionary: [{'id':i, 'name':dictionary[i]} for i in dictionary]


def get_cache():
    return CacheManager.getInstance().cache

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)
    
def months_between_dates(from_date=None, to_date=None):
    if not (from_date and to_date):
        now = time.localtime()
        return [time.localtime(time.mktime((now.tm_year, now.tm_mon - n,
                                            1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(6)
                ]
    if not to_date:
        to_date = datetime.today()
    if not from_date:
        from_date = (to_date - timedelta(days=30 * 6)).date()
    iter_month = from_date.month
    iter_year = from_date.year
    months_list = []
    if from_date > to_date:
        from_date, to_date = to_date, from_date
    while not(iter_month == to_date.month and iter_year == to_date.year):
        months_list.append((iter_year, iter_month))
        iter_month += 1
        if iter_month > 12:
            iter_month = 1
            iter_year += 1
    months_list.append((iter_year, iter_month))
    return reversed(sorted(months_list, key=lambda x: (x[0], x[1]), reverse=True))
