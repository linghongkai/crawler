from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    isSelected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Info(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.title
