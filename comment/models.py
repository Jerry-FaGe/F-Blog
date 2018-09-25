from django.db import models
from blog.models import Blog
from userapp.models import User
# Create your models here.
class Comment(models.Model):
    comment_title=models.ForeignKey(Blog,on_delete=models.DO_NOTHING)
    text=models.TextField()#评论内容
    comment_time=models.DateTimeField(auto_now_add=True)
    comment_user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
