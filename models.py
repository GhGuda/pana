from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    back_img = models.ImageField(upload_to="back_images", default="thin.jpg")
    profile_img = models.ImageField(upload_to="profile_images", default="blank.webp")
    location = models.CharField(max_length=400, blank=True)
    job = models.CharField(max_length=400, blank=True)
    bio = models.TextField(blank=True)
    display_name = models.CharField(max_length=50)
    web = models.URLField(blank=True)
    follw = models.IntegerField(default=0)
    follwing = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
            


    class Meta:
        
        verbose_name_plural = 'Profile'



class Trend(models.Model):
    tag = models.CharField(max_length=200)
    post_count = models.IntegerField(default=0)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name_plural = 'Trends'



class Posts(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_id = models.UUIDField(default=uuid.uuid4)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    caption = models.TextField()
    trends = models.ForeignKey(Trend, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    saved = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    schedule = models.DateTimeField(auto_now_add=False, null=True)
    
    def __str__(self):
       return f"{self.profile.user.username.upper()} posted {self.caption}"
    
    class Meta:
        verbose_name_plural = 'Post'



class Like_post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_id = models.TextField()

    def __str__(self):
        return f"{self.user.user.username.upper()} liked {self.post_id}"
    
    class Meta:
        verbose_name_plural = 'Post Likes'




class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment_id = models.UUIDField(default=uuid.uuid4)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username.upper()} commented on {self.post}"
    
    class Meta:
        verbose_name_plural = 'Comment'


class Like_comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_id = models.TextField()

    def __str__(self):
        return f"{self.user.user.username.upper()} liked {self.comment_id}"
    
    class Meta:
        verbose_name_plural = 'Comment Likes'


class Follow(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')


    def __str__(self):
        return f"{self.user.user.username} is following  {self.following.user.username}"
    
    class Meta:
        verbose_name_plural = 'Follow'

