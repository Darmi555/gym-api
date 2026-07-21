from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from gym.models import User, Gym, Studio, Trainer, Discipline, TrainingSession, Reservation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Gym profile", {"fields": ("phone_number", "date_of_birth", "membership_level")}),
    )
    list_display = ("id", "email", "username", "membership_level", "is_staff")


admin.site.register(Gym)
admin.site.register(Studio)
admin.site.register(Trainer)
admin.site.register(Discipline)
admin.site.register(TrainingSession)
admin.site.register(Reservation)
