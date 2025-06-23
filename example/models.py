from django.db import models


class First(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Second(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title


class Third(models.Model):
    heading = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self) -> str:
        return self.heading
