from datetime import date, datetime
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Student, Lesson
from .serializers import LessonListSerializer, LessonSerializer, ScheduleResponseSerializer


class LessonViewSet(ReadOnlyModelViewSet):
    """GET /api/lessons/ — список всех уроков."""
    queryset = Lesson.objects.select_related('group', 'subject', 'room').order_by('day_of_week', 'order')
    serializer_class = LessonListSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """GET /api/schedule/?tg_login=username&date=2025-02-26"""
    queryset = Lesson.objects.select_related('subject', 'room', 'group')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        tg_login = request.query_params.get('tg_login', '').strip()
        if not tg_login:
            return Response(
                {'error': 'tg_login required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        date_param = request.query_params.get('date')
        if date_param:
            try:
                target_date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'date must be YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = date.today()

        try:
            student = Student.objects.select_related('group').get(tg_login=tg_login)
        except Student.DoesNotExist:
            return Response(
                {'error': 'not_found'},
                status=status.HTTP_404_NOT_FOUND
            )

        day_of_week = target_date.weekday()
        lessons = self.queryset.filter(
            group=student.group,
            day_of_week=day_of_week
        ).order_by('order')

        response_data = {
            'date': target_date,
            'group': student.group.name,
            'lessons': lessons,
        }
        return Response(ScheduleResponseSerializer(response_data).data)

        