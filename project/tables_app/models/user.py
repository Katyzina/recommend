from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, verbose_name="Отчество")
    email = models.EmailField(verbose_name="Почта")
    phone_number = models.CharField(max_length=50,
                                    verbose_name="Номер телефона")
    image = models.ImageField(upload_to="users/", verbose_name="Изображение")

    student = models.ForeignKey("Student", on_delete=models.SET_NULL,
                                null=True, blank=True, verbose_name="Студент")
    employer = models.ForeignKey("Employer", on_delete=models.SET_NULL,
                                 null=True, verbose_name="Работодатель")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
