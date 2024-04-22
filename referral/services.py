import random
import string


def generate_referral_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join((random.choice(chars) for i in range(6)))


def generate_confirmation_code():
    return ''.join((random.choice(string.digits) for i in range(4)))
