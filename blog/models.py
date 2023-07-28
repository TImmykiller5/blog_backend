from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django_summernote.widgets import SummernoteWidget


# Create your models here.
class Tags(models.Model):
    tagName = models.CharField(
            max_length=30,
            validators=[MinLengthValidator(1, "Title must be greater than 5 characters")],
            unique=True
            
    )

    def __str__(self):
        return self.tagName


class BlogPost(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(5, "Title must be greater than 5 characters")]
    )
    text = models.TextField()
    tag = models.ManyToManyField(to=Tags, related_name="posts", blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, related_name='forums_owned')
    # comments = models.ManyToManyField(settings.AUTH_USER_MODEL, 
    #     through='Comment', related_name='forum_comments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


    