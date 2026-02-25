from django.db import models


class Group(models.Model):
    """Группа: 2 символа — год обучения + буква класса (1А, 2Б)."""
    name = models.CharField(max_length=2, unique=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Room(models.Model):
    """Кабинет с номером."""
    number = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return str(self.number)


class Subject(models.Model):
    """Предмет."""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Урок: группа, предмет, кабинет, день недели, порядок."""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='lessons')
    day_of_week = models.IntegerField()  # 0=пн, 6=вс
    order = models.IntegerField()  # порядок урока в дне (1, 2, 3...)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['day_of_week', 'order']
        unique_together = [['group', 'day_of_week', 'order']]

    def __str__(self):
        return f"{self.group} {self.subject} #{self.order}"


class Student(models.Model):
    """Студент с tg_login (username) и группой."""
    tg_login = models.CharField(max_length=64, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f"{self.tg_login} ({self.group})"
