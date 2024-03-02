from django.db import models


class Institute(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "Institutes"  # название таблицы в бд
        verbose_name = "Институт"  # название таблицы в админке
        verbose_name_plural = "Институты"  # название таблицы в админке
