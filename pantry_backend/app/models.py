from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturalday


class Location(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()

    def __str__(self):
        return self.name


class ConsumableQuerySet(models.QuerySet):
    def get_expires_in_days(self, days):
        now = timezone.now().date()
        expiry_threshold = now + timezone.timedelta(days)
        return self.filter(expiry__lte=expiry_threshold)

    # Accepts YYYY-mm-dd, e.g., 2020-01-01
    def get_expires_by_date(self, date):
        converted_date = datetime.strptime(date, "%Y-%m-%d")
        return self.filter(expiry__lte=date)


class ConsumableManager(models.Manager):
    def get_queryset(self):
        return ConsumableQuerySet(self.model, using=self._db)


class Consumable(models.Model):
    name = models.CharField(max_length=48)
    description = models.TextField()
    count = models.IntegerField(default=1)
    expiry = models.DateField(blank=True)
    locations = models.ManyToManyField(Location, related_name='consumables')

    consumables = ConsumableManager()

    def __str__(self):
        return self.name

    def get_human_date_expiry(self):
        return naturalday(self.expiry)

    def get_days_to_expiry(self):
        now = timezone.now().date()
        days_to_expiry = (self.expiry - now).days
        return days_to_expiry
