from django.db import models

class Consumable(models.Model):
    name = models.CharField()
    description = models.TextField()
    count = models.IntegerField()
    expiry = models.DateField()
    # location = models.ManyToManyField(Location)

    def __str__(self):
        return self.name
