from django.db import models
from django.utils import timezone
from authentication.models import User


# This file will contain your data models as the project grows.
# For now, we'll create some basic models that align with your project outline.

class Unit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_unit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='child_units')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserUnit(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('leader', 'Leader'),
        ('admin', 'Administrator'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_memberships')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'unit')

    def __str__(self):
        return f"{self.user.username} - {self.unit.name} ({self.role})"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EventAttendee(models.Model):
    STATUS_CHOICES = [
        ('attending', 'Attending'),
        ('declined', 'Declined'),
        ('tentative', 'Tentative'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='tentative')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    is_pinned = models.BooleanField(default=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='announcements', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title