from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name', read_only=True)
    room = serializers.CharField(source='room.number', read_only=True)

    class Meta:
        model = Lesson
        fields = ['order', 'subject', 'room']


class LessonListSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name', read_only=True)
    subject = serializers.CharField(source='subject.name', read_only=True)
    room = serializers.CharField(source='room.number', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'group', 'subject', 'room', 'day_of_week', 'order']


class ScheduleResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    group = serializers.CharField()
    lessons = LessonSerializer(many=True)
