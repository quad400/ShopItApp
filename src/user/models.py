from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


# Create your models here.

class UserAccount(AbstractUser):

    # class Meta(AbstractUser.Meta):
    #     swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True,  null=True)
    zip = models.CharField(max_length=100, blank=True,  null=True)
    city = models.CharField(max_length=100, blank=True,  null=True)
    country = models.CharField(max_length=100, blank=True,  null=True)
    image = models.ImageField(blank=True, upload_to='images/users/', null=True)

    def __str__(self):
        return self.user.username