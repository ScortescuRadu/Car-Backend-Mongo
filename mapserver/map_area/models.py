from django.db import models

# Create your models here.
class GeoJsonFeature(models.Model):
    geojson = models.JSONField()
    description = models.CharField(max_length=255, blank=True, null=True)