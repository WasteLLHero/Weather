from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    time = models.DateField(auto_now=True)
    city = models.TextField()
    count = models.IntegerField(default=1)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    def __str__(self) -> str:
        return str(self.city)