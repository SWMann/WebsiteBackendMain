from django.contrib import admin
from .models import Unit, UserUnit, Event, EventAttendee, Announcement

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_unit', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(UserUnit)
class UserUnitAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'role', 'joined_at')
    list_filter = ('role', 'joined_at', 'unit')
    search_fields = ('user__username', 'unit__name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'location', 'creator', 'unit')
    list_filter = ('start_time', 'unit')
    search_fields = ('title', 'description', 'location', 'creator__username')
    date_hierarchy = 'start_time'

@admin.register(EventAttendee)
class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'event__title')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_pinned', 'unit', 'created_at')
    list_filter = ('is_pinned', 'created_at', 'unit')
    search_fields = ('title', 'content', 'author__username')