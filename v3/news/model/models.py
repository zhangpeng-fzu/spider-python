from django.db import models


# Create your models here.
class User(models.Model):
    ACCOUNT = models.CharField(max_length=32, default="")
    PASSWORD = models.CharField(max_length=32, default="")
    ROLE = models.CharField(max_length=10, default="")
    CREATE_TIME = models.DateTimeField()

    class Meta:
        db_table = "user"


class News(models.Model):
    NEWS_ID = models.TextField(max_length=32, default="")
    TITLE = models.TextField(max_length=32, default="")
    AUTHOR = models.CharField(max_length=255, default="")
    URL = models.CharField(max_length=255, default="")
    KEYWORDS = models.CharField(max_length=100, default="")
    SOURCE = models.CharField(max_length=16, default="")
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "news"
