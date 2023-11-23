from django.db import models
from django.utils import timezone
from django.urls import reverse
# reverse() is a function that returns the URL for a given view and optional parameters.


# Create your models here.
class Post(models.Model):
    # author is actually connected to the auth.User model ie superuser
    # each author will be linked to a single post
    # foreign key actually links to another model and the 'auth.User' is the application name and the model name
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True)
    # published date can be blank and null because we don't want to publish the post right away.
    # blank=True means that the field is optional and null=True means that the database column will be null.

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        # this is a query set that will return only the approved comments

    def get_absolute_url(self): # name of function is important as it is predefined  by Django
        return reverse('post_detail',kwargs={'pk':self.pk})
        # post_detail is the name of the view that we want to redirect to
        # kwargs is a dictionary that maps the pk variable from urls.py to the pk of the current post

    def __str__(self):
        return self.title


class Comment(models.Model):
    # each comment will be linked to a single post

    # foreign key actually links to another model and the 'blog.Post' is the application name and the model name
    post=models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()


    # it tells Django where to go when we create a new comment i.e. where website should redirect us
    def get_absolute_url(self): # name of function is important as it is predefined  by Django
        return reverse('post_list')

    def __str__(self):
        return self.text


