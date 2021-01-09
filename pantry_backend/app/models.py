from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()

    def __str__(self):
        return self.name


class Consumable(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()
    count = models.IntegerField()
    expiry = models.DateField()
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.name
