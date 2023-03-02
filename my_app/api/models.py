from django.db import models
from django.conf import settings


class Task(models.Model):
    header = models.CharField(blank=False, max_length=100, verbose_name="Заголовок")
    text = models.TextField(blank=False, verbose_name="Текст задачи")
    date_of_completion = models.DateTimeField(verbose_name="Дата выполнения")
    is_completed = models.BooleanField(default=False, verbose_name="Задача завершена")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
