from django.db import models


class Employer(models.Model):
    organization = models.CharField(max_length=50, verbose_name="Организация")

    def __str__(self):
        return f"{self.organization}"

    class Meta:
        db_table = "employers"  # название таблицы в бд
        verbose_name = "Работодатель"  # название таблицы в админке
        verbose_name_plural = "Работодатели"  # название таблицы в админке
