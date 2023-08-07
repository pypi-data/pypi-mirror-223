from django.core.validators import RegexValidator
import re
from django.conf import settings
from functools import wraps


# Regualr expression  VALID CODE
valid_phone = RegexValidator(
    r"^[1-9][0-9]{9}$", "Phone number should be 10 digit number")
valid_price = RegexValidator(
    r"^[1-9][0-9]*[.]?[0-9]{0,2}$", "Please enter a valid price")
valid_text = RegexValidator(
    r"^[#.0-9a-zA-Z\s,-/%~`!@$&*\(\)_=\+\}\]\{\[\|\''"";:?/]+$", "Special characters are not allowed")
valid_only_text = RegexValidator(
    r"^[a-zA-Z]+$", "Special characters are not allowed")
valid_char = RegexValidator(
    r"^[a-zA-Z\s]+$", "Special characters are not allowed")
valid_number = RegexValidator(
    r"^[1-9][0-9]+$", "Please enter a Number")
valid_float = RegexValidator(
    r"^[1-9][0-9]*[.]?[0-9]{0,2}$", "Please enter a Value")
valid_password = RegexValidator(
    r"^(?=.*\d)[a-zA-Z0-9$!@#%^&*()-_+/~]{8,}$", "At least 8 characters and 1 digit")
valid_address = RegexValidator(
    r"^[#.0-9a-zA-Z\s,-/%~`!@$&*\(\)_=\+\}\]\{\[\|\''"";:?/]+$", "Address is not valid")
valid_gst = RegexValidator(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", 'Invalid GSTIN number')
valid_pan = RegexValidator(
    r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", 'Invalid GSTIN number')
valid_bank = RegexValidator(r"^[0-9]{9,18}$", 'Invalid GSTIN number')
valid_ifsc = RegexValidator(r"^[A-Z]{4}0[A-Z0-9]{6}$", 'Invalid GSTIN number')
valid_coupon_code = RegexValidator(
    r'^[a-zA-Z]{1}[a-zA-Z0-9-%]+', 'Invalid coupon code')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# disbable signal when loddata from fixtures(sakib)


def disable_signal(signal_handler):
    """
        Decorator that turns off signal handlers when loading fixture data.
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if 'raw' in kwargs and kwargs.get('raw'):
            return
        return signal_handler(*args, **kwargs)
    return wrapper


def get_m2m_obj(data, model_obj):
    objects = []
    for id in data:
        objects.append(model_obj.objects.filter(id=id).first())
    return objects


def rreplace(value, word):
    try:
        return ''.join(str(value).rsplit(word, 1))
    except:
        return ''


def convert_to_hifn(val):
    pattern = re.compile(r"""[\s&\/\\#,@+()$~%.'":*?<>{}]""")
    return pattern.sub("-", str(val).lower())

# Encryption algorithm created SAKIB MALIK


def encrypt_secret_key(plain_text):
    trans_str = ''
    for word in plain_text:
        trans_str += str(ord(word)+3)+'S'
    return trans_str.strip('S')


def encrypt_msg(plain_text):
    if 'ENCRYPTION_SECRECT_KEY' in settings:
        ENCRYPTION_SECRECT_KEY = settings.ENCRYPTION_SECRECT_KEY
        public_key = encrypt_secret_key(ENCRYPTION_SECRECT_KEY)
        trans_str = ''
        for word in str(plain_text):
            trans_str += str(ord(word)+3)+'M'
        return public_key+trans_str.strip('M')
    else:
        raise Exception(
            'Please Declare \"ENCRYPTION_SECRECT_KEY\" in settinsgs.py project file')


def deccrypt_msg(cipher_text):
    if 'ENCRYPTION_SECRECT_KEY' in settings:
        ENCRYPTION_SECRECT_KEY = settings.ENCRYPTION_SECRECT_KEY
        public_key = encrypt_secret_key(ENCRYPTION_SECRECT_KEY)
        trans_str = ''
        for word in str(cipher_text).replace(public_key, '', 1).split('M'):
            trans_str += chr(int(word)-3)
        return trans_str
    else:
        raise Exception(
            'Please Declare \"ENCRYPTION_SECRECT_KEY\" in settinsgs.py project file')
