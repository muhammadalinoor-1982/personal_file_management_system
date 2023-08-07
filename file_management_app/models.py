from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    auth_token  = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_on  = models.DateTimeField(auto_now_add=True)

class exam(models.Model):
        SEX = (
            ('male', 'male'),
            ('female', 'female'),
            ('others', 'others')
        )

        name = models.CharField(max_length=50, null=True, blank=True)
        image = models.ImageField(upload_to='exam_pic/', default='default/no_img.jpg', null=True, blank=True)
        sex = models.CharField(max_length=30, choices=SEX)

        def __str__(self):
            return str(self.user.username)

