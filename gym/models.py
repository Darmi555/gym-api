from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    class MembershipLevel(models.TextChoices):
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    phone_number = models.CharField(max_length=11, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    membership_level = models.CharField(choices=MembershipLevel.choices, default=MembershipLevel.BASIC, max_length=20)



class Gym(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=128)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.location})"


class Studio(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="studios")
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Trainer(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    experience_years = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Discipline(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class TrainingSession(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="sessions")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="sessions")
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.discipline}: {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M --- %Y-%m-%d ')}"



class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name="reservations")
