from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(null=True)
    pic = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "created on %s - %s"%(self.created, self.title)