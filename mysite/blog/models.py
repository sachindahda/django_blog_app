from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    #Third Party Software The tags manager will allow you to add, retrieve, and remove tags from Post objects.
    tags=TaggableManager()

    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=200,unique_for_date='publish')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.   
    # We have added a Meta class inside the model. This class defines metadata for the model. We use the
    # ordering attribute to tell Django that it should sort results by the publish field. This ordering will
    # apply by default for database queries when no specific order is provided in the query. We indicate
    # descending order by using a hyphen before the field name, -publish. Posts will be returned in reverse
    # chronological order by default.
    class Meta:
        ordering = ['-publish']


        # We have added the indexes option to the model’s Meta class. This option allows you to define database
        # indexes for your model, which could comprise one or multiple fields, in ascending or descending
        # order, or functional expressions and database functions. We have added an index for the publish
        # field. We use a hyphen before the field name to define the index in descending order. The creation of
        # this index will be included in the database migrations that we will generate later for our blog models.
        indexes = [
            models.Index(fields=['-publish']),
        ]

    
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        # return reverse('blog:post_detail',args=[self.id])
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self. slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'