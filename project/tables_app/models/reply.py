from django.db import models


class Reply(models.Model):
    student = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Студент")
    vacation = models.ForeignKey("Vacation", on_delete=models.CASCADE, verbose_name="Вакансия")

    def __str__(self):
        return f"{self.student.first_name} - {self.vacation.position}"

    class Meta:
        db_table = "reply"
        verbose_name = "Отклики"
        verbose_name_plural = "Отклики"
