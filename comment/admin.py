from django.contrib import admin
from.models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_title','text','comment_time','comment_user')