from django.db import models


class Support(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    description = models.TextField(max_length=500, verbose_name="Проблема пользователя")
    email = models.EmailField(verbose_name="Почта")
    image = models.ImageField(upload_to="supports/", verbose_name="Изображение")

    def __str__(self):
        return f"{self.username} {self.description}"

    class Meta:
        db_table = "supports"  # название таблицы в бд
        verbose_name = "Поддержка"  # название таблицы в админке
        verbose_name_plural = "Поддержка"  # название таблицы в админке
