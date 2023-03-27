from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name='following_user', blank=True)
    friends = models.ManyToManyField(User, related_name='friends_user', blank=True)
    bio = models.CharField(max_length=150, blank=True)
    date_birth = models.DateField(blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default_profile.png', upload_to='profiles_img', blank=True, null=True)

    def profile_posts(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def __str__(self):
        return f'Profile {self.user.username}'


class Relationship(models.Model):
    STATUS_CHOICES = (
        ('send', 'send'),
        ('accepted', 'accepted')
    )
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} -> {self.receiver} = {self.status}'
