import hmac

from base64 import b64encode
from hashlib import sha256

from django.utils.crypto import constant_time_compare


def basic_token(key, secret):
    # concatenate the strings to force TypeError
    token = b64encode(bytes(key + ':' + secret, 'utf-8')).decode('utf-8')
    return 'Basic ' + token


def timesafe_mac_compare(signature, client_secret, data):
    client_bytes = bytes(client_secret, 'utf-8')
    signed_data = hmac.new(client_bytes, data, sha256).hexdigest()
    return constant_time_compare(signature, signed_data)
