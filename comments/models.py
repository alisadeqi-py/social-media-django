from django.db import models
from django.contrib.auth.models import User
from home.models import Post
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE , related_name='pcomments')
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE , related_name='rcomment' , blank=True , null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.body[:30]}-{self.created}'