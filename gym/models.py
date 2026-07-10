from django.db import models

class Gym(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=128)
    open_time = models.TimeField()
    close_time = models.TimeField()



