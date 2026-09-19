from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile_user_id = models.IntegerField()
    display_name = models.CharField(max_length=80)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default='blank_profile_image.png', blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name or self.user.username