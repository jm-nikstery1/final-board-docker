from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

MyUser = get_user_model()

class Post(models.Model):

    user = models.ForeignKey(MyUser,
                                on_delete=models.CASCADE,
                                related_name='posts',
                             )
    subject = models.CharField(max_length=128)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    likes = models.ManyToManyField(MyUser, related_name='liked_posts', blank=True)


class Comment(models.Model):
    user = models.ForeignKey(MyUser,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    likes = models.ManyToManyField(MyUser, related_name='liked_comments', blank=True)
