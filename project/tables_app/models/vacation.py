from django.db import models


class Vacation(models.Model):
    position = models.CharField(max_length=50, verbose_name="Должность")
    description = models.TextField(max_length=500, verbose_name="Описание")
    image = models.ImageField(upload_to="vacations/", verbose_name="Изображение")

    city = models.ForeignKey("City", on_delete=models.SET_NULL, null=True, verbose_name="Город")
    institute = models.ForeignKey("Institute", on_delete=models.SET_NULL, null=True, verbose_name="Институт")
    employer = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Работодатель")

    FULL = "FULL"
    FLEXIBLE = "FLEXIBLE"
    SHIFT_WORK = "SHIFT_WORK"

    BUSYNESS_CHOICE = (
        (FULL, "Полная занятось"),
        (FLEXIBLE, "Гибкий график"),
        (SHIFT_WORK, "Сменный график")
    )

    busyness = models.CharField(max_length=10, choices=BUSYNESS_CHOICE, default=FULL, verbose_name="Занятость")
    skills = models.CharField(max_length=255, verbose_name="Ключевые навыки")
    address = models.CharField(max_length=150, verbose_name="Адрес")

    def __str__(self):
        return f"{self.position} {self.employer.first_name} {self.employer.phone_number}  "

    class Meta:
        db_table = "vacations"
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
