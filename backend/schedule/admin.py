from django.contrib import admin
from .models import Group, Room, Subject, Lesson, Student


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject', 'room', 'day_of_week', 'order')
    list_filter = ('group', 'day_of_week')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('tg_login', 'group')
    search_fields = ('tg_login',)
