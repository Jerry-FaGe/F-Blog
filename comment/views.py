from django.shortcuts import render,redirect,get_object_or_404
from .models import Comment
from userapp.models import User
# Create your views here.
def update_comment(request):

    text=request.POST.get('text')
    comment_title_id=request.POST.get('title')
    user=request.POST.get('user')
    user_object = User.objects.get(name=user)
    comment_user_id = user_object.id
    comment=Comment()
    comment.text=text
    comment.comment_title_id=comment_title_id
    comment.comment_user_id=comment_user_id
    comment.save()
    blog_id=int(comment_title_id)
    return redirect('/blog/%s'%blog_id)