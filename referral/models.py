import random
import string

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from referral.services import generate_referral_code


# Create your models here.

class UserManager(BaseUserManager):
    
    def create(self, phone_number, **kwargs):

        chars = string.ascii_letters + string.digits
        is_code_created = False

        while not is_code_created:
            code_value = generate_referral_code()

            try:
                user_with_code = self.get(code=code_value)
            except ObjectDoesNotExist:
                user_with_code = None
            
            if user_with_code:
                continue

            is_code_created = True

        user = self.model(phone_number=phone_number, code=code_value)
        user.save()

        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6, unique=True, editable=False)

    is_confirmed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def has_usable_password(self):
        return False

    def set_password(self, raw_password):
        pass


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_codes')
    conf_code = models.CharField(max_length=4)

class ReferredUsers(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='users_referrers', editable=False)
    referral = models.OneToOneField(User, on_delete=models.PROTECT, related_name='users_referrals', editable=False)
