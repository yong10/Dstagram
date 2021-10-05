from django.db import models
import re
from PIL import Image

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
            
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First Name must be at least 2 characters!"

        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last Name must be at least 2 characters!"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        all_users = User.objects.all()
        for x in all_users:
            if x.email == postData['email']:
                errors['email'] = "Email must be unique!"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"

        if postData['password'] != postData['cPassword']:
            errors['password'] = "Password does not match password confirm!"
        return errors

class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['commentText']) < 1:
            errors['commentText'] = "Comment can not be empty! "
        return errors

class User(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
        
class Photo(models.Model):
    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'timeline_photo/%Y/%m/%d')
    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    commentText = models.TextField(blank=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    photoCommented = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()