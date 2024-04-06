from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "cities"  # название таблицы в бд
        verbose_name = "Город"  # название таблицы в админке
        verbose_name_plural = "Города"  # название таблицы в админке
