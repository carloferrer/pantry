from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone


class Location(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()

    def __str__(self):
        return self.name


class Consumable(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()
    count = models.IntegerField(default=1)
    expiry = models.DateField(blank=True)
    locations = models.ManyToManyField(Location, related_name='consumables')

    def __str__(self):
        return self.name

    def get_human_date_expiry(self):
        return naturalday(self.expiry)

    def get_days_to_expiry(self):
        now = timezone.now().date()
        days_to_expiry = (self.expiry - now).days
        return days_to_expiry
