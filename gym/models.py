from django.db import models


class Gym(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=128)
    open_time = models.TimeField()
    close_time = models.TimeField()


class Studio(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="studios")
    capacity = models.PositiveIntegerField()

