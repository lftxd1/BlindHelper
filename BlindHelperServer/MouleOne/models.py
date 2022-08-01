from django.db import models


# Create your models here.
class Article(models.Model):
    content = models.TextField()
    classes = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    click = models.IntegerField()

