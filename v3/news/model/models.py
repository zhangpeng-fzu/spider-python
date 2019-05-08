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
    NEWS_ID = models.CharField(max_length=32, default="")
    TITLE = models.TextField(max_length=32, default="")
    AUTHOR = models.CharField(max_length=255, default="")
    URL = models.CharField(max_length=255, default="")
    KEYWORDS = models.CharField(max_length=100, default="")
    SOURCE = models.CharField(max_length=16, default="")
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "news"


class Role(models.Model):
    ROLE_NAME = models.CharField(max_length=32, default="")
    DESCRIPTION = models.CharField(max_length=32, default="")
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "role"


class Label(models.Model):
    NAME = models.CharField(max_length=32, default="")
    DESCRIPTION = models.CharField(max_length=32, default="")
    ENABLE = models.IntegerField(default=0)
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "news_label"


class WhiteIP(models.Model):
    IP = models.CharField(max_length=32, default="")
    NAME = models.CharField(max_length=32, default="")
    ENABLE = models.IntegerField(default=0)
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "white_ip_list"


class AntiConfig(models.Model):
    STRATEGY = models.CharField(max_length=32, default="")
    DESCRIPTION = models.CharField(max_length=32, default="")
    ENABLE = models.IntegerField(default=0)
    CREATE_TIME = models.CharField(max_length=20, default="")

    class Meta:
        db_table = "anti_config"
