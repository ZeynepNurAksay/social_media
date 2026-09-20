from django.db import models
from django.contrib.auth import get_user_model
import uuid

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

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    text = models.CharField(max_length=2200, blank=True)
    caption = models.TextField(max_length=2200, blank=True)
    image = models.ImageField(upload_to="posts/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.author.display_name} ({self.created_at:%Y-%m-%d})"

class Like(models.Model):
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes_posts")
    liked_by = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="liked_by",
    )