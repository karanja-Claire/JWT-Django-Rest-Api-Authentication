from myapi.models import User, Code
from myapi.services.email_srevices import Email
from datetime import datetime, timedelta, date
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
import string
import random
import pytz
class UserService:
    

    @staticmethod
    def generate_random_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    @staticmethod
    def calculate_expiry_time():
        """Calculating expiry time for verification code"""
        updated_time = datetime.now() + timedelta(hours=24)
        return updated_time

    def create_verification_code(self,activate_code , user) :
        expiry = self.calculate_expiry_time()
        # print('yes',user.id , expiry)
        return Code.objects.create(user_id=user.id, code=activate_code, expiry=expiry)

    def send_verification_email(self, email_subject, email_body, user):
        activate_code = self.generate_random_code()
        this_user = user.id
        print(user.id,activate_code)
        expiry = self.calculate_expiry_time()
        Code.objects.create(user_id=user.id, code=activate_code, expiry=expiry)
        # self.create_verification_code(user, activate_code)

        email_body = email_body + activate_code
        Email.send(email_subject, email_body, [user.email])
        return activate_code

    # def register_user(self, kwargs):
    #     user = User.objects.create_user(**kwargs)
    #     email_subject = 'Activate your Account'
    #     email_body = 'Your activation code is '
    #     self.send_verification_email(email_subject, email_body, user)
    #     return user
