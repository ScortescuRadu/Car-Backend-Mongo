from django.db import models

# Create your models here.
class Marker(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()