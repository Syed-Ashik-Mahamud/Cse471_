from django.db import models

# Create your models here.
from datetime import datetime
import os


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s-%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)


class UserModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=1024)
    phoneNumber = models.CharField(max_length=15)
    completeProfile = models.CharField(max_length=5)
    location = models.CharField(max_length=50)

    class Meta:
        db_table = 'app_users'

    def isExists(self):
        if UserModel.objects.filter(email=self.email):
            return True
        return False


class ResetPwdTokens(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reset_pwd_tokens'

    def __str__(self):
        return self.user.email


class UserContact(models.Model):
    messengerId = models.CharField(max_length=10)
    messengerName = models.CharField(max_length=50)
    messengerEmail = models.CharField(max_length=40)
    message = models.CharField(max_length=3072)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_contacts'







